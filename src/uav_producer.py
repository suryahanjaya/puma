import sqlite3
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- Konfigurasi Path ---
DATA_DIR = "data" 
DB_PATH = os.path.join(DATA_DIR, "uav_telemetry.db")
CSV_PATH = os.path.join(DATA_DIR, "telemetry_data.csv")
# ------------------------

def init_db():
    """
    Inisialisasi database SQLite dan membuat tabel telemetry.
    Impor CSV dinonaktifkan untuk memulai baru.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    csv_path = CSV_PATH
    
    if os.path.exists(csv_path):
        df_header = pd.read_csv(csv_path, nrows=1)
        columns = df_header.columns.tolist()
        print(f"✓ Ditemukan {len(columns)} kolom dari CSV di {csv_path}")
    else:
        print(f"⚠ CSV tidak ditemukan di {csv_path}, menggunakan struktur default")
        columns = [
            "timestamp", "dt", "date", "altitude", "gps_alt", "gps_lat", "gps_lon",
            "heading", "pitch", "roll", "yaw", "ground_speed", "airspeed", "vertical_speed",
            "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z",
            "battery_level", "battery_voltage", "battery_current", "temperature_battery",
            "motor_rpm_1", "motor_rpm_2", "motor_rpm_3", "motor_rpm_4",
            "motor_temp_1", "motor_temp_2", "motor_temp_3", "motor_temp_4",
            "throttle_position", "payload_weight", "lidar_altitude", "obstacle_distance",
            "sat_count", "gps_fix_type", "link_quality", "signal_strength",
            "mode", "system_status", "mission_id", "waypoint_id", "event"
        ]
    
    def get_sqlite_type(col_name):
        if col_name in ["timestamp", "sat_count", "gps_fix_type", "waypoint_id"]:
            return "INTEGER"
        elif col_name in ["dt", "date", "mode", "system_status", "mission_id", "event"]:
            return "TEXT"
        else:
            return "REAL"
    
    column_defs = [f"{col} {get_sqlite_type(col)}" for col in columns]
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS telemetry (
        {', '.join(column_defs)}
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("✓ Tabel 'telemetry' berhasil dibuat/diverifikasi")
    
    if os.path.exists(csv_path):
        try:
            cursor.execute("SELECT COUNT(*) FROM telemetry")
            existing_count = cursor.fetchone()[0]
            
            if existing_count == 0:
                print("✓ Database kosong. Melewatkan impor CSV untuk memulai simulasi baru.")
            else:
                print(f"✓ Database sudah berisi {existing_count} baris data (melewati import CSV)")
        except Exception as e:
            print(f"⚠ Error saat memuat data historis: {e}")
    
    conn.close()
    return columns


def get_last_row_template(cursor, columns):
    """Mengambil baris terakhir dari database sebagai templat"""
    cursor.execute("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        return dict(zip(columns, row))
    else:
        print("✓ Database kosong, memulai simulasi baru dari 0m.")
        return {
            "timestamp": int(time.time()),
            "dt": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "date": datetime.now().strftime("%Y/%m/%d"),
            "altitude": 0.0, "gps_alt": 0.0,
            "gps_lat": -7.27, "gps_lon": 112.74,
            "heading": 90.0, "pitch": 0.0, "roll": 0.0, "yaw": 90.0,
            "ground_speed": 0.0, "airspeed": 0.0, "vertical_speed": 0.0,
            "accel_x": 0.0, "accel_y": 0.0, "accel_z": 0.0,
            "gyro_x": 0.0, "gyro_y": 0.0, "gyro_z": 0.0,
            "battery_level": 100.0, "battery_voltage": 14.8,
            "battery_current": 0.0, "temperature_battery": 25.0,
            "motor_rpm_1": 0.0, "motor_rpm_2": 0.0, "motor_rpm_3": 0.0, "motor_rpm_4": 0.0,
            "motor_temp_1": 25.0, "motor_temp_2": 25.0, "motor_temp_3": 25.0, "motor_temp_4": 25.0,
            "throttle_position": 0.0, "payload_weight": 0.0,
            "lidar_altitude": 0.0, "obstacle_distance": 100.0,
            "sat_count": 10, "gps_fix_type": 3,
            "link_quality": 80.0, "signal_strength": -80.0,
            "mode": "Auto", "system_status": "Landed",
            "mission_id": "M002", "waypoint_id": 0, "event": ""
        }


def generate_new_telemetry(template, state):
    """Generate data telemetri baru berdasarkan templat dan state penerbangan"""
    new_data = template.copy()
    
    new_data["timestamp"] = int(time.time())
    current_time = datetime.now()
    new_data["dt"] = current_time.strftime("%Y/%m/%d %H:%M:%S")
    new_data["date"] = current_time.strftime("%Y/%m/%d")

    # --- [ DIPINDAHKAN KE ATAS ] ---
    # Kalkulasi baterai harus terjadi SEBELUM pengecekan fase
    if state["phase"] != "LANDED":
        battery_decrease = random.uniform(0.05, 0.10)
        new_data["battery_level"] = max(5, new_data.get("battery_level", 100.0) - battery_decrease)
    
    new_data["battery_voltage"] = 14.8 * (new_data["battery_level"] / 100) + random.uniform(-0.1, 0.1)
    new_data["battery_current"] = random.uniform(5, 25) if state["phase"] != "LANDED" else 0
    new_data["temperature_battery"] = random.uniform(20, 45)
    # --- [ AKHIR BAGIAN DIPINDAHKAN ] ---


    # --- Logika "U-Turn" / RTL jika Baterai Habis ---
    LOW_BATTERY_THRESHOLD = 25.0 
    
    if state["phase"] in ["CLIMB", "CRUISE"] and new_data["battery_level"] < LOW_BATTERY_THRESHOLD:
        state["phase"] = "DESCEND" # Paksa "Return to Launch" (Descend)
        new_data["mode"] = "RTL"    # Set mode ke RTL
        new_data["event"] = "Low Battery U-Turn"
        print(f"--- ⚠️  Baterai < {LOW_BATTERY_THRESHOLD}%. Memulai U-TURN (DESCEND) ---")
    
    # --------------------------------------------------

    
    new_data["ground_speed"] = random.uniform(10, 70)
    new_data["airspeed"] = new_data["ground_speed"] + random.uniform(-2, 2)

    current_altitude = new_data.get("altitude", 0.0)
    phase = state["phase"]
    
    if phase == "CLIMB":
        altitude_change = state["climb_rate"] + random.uniform(-1, 1)
        new_data["altitude"] = max(0, current_altitude + altitude_change)
        new_data["vertical_speed"] = altitude_change
        new_data["mode"] = "Auto"
        
        if new_data["altitude"] >= state["target_altitude"]:
            new_data["altitude"] = state["target_altitude"]
            state["phase"] = "CRUISE"
            state["cruise_start_time"] = time.time()
            new_data["vertical_speed"] = 0
            print("--- ⬆️  Fase berubah: CLIMB -> CRUISE ---")

    elif phase == "CRUISE":
        altitude_change = random.uniform(-1.5, 1.5)
        new_data["altitude"] = state["target_altitude"] + altitude_change
        new_data["vertical_speed"] = altitude_change
        new_data["mode"] = "Auto"
        
        elapsed_cruise = time.time() - state["cruise_start_time"]
        if elapsed_cruise >= state["cruise_duration_seconds"]:
            state["phase"] = "DESCEND"
            print("--- ➡️  Fase berubah: CRUISE -> DESCEND ---")

    elif phase == "DESCEND":
        altitude_change = state["descend_rate"] + random.uniform(-1, 1)
        new_data["altitude"] = max(0, current_altitude + altitude_change)
        new_data["vertical_speed"] = altitude_change
        new_data["mode"] = "RTL" 
        
        if new_data["altitude"] <= 0:
            new_data["altitude"] = 0
            state["phase"] = "LANDED"
            state["landed_time"] = time.time()
            new_data["vertical_speed"] = 0
            print("--- ⬇️  Fase berubah: DESCEND -> LANDED ---")

    elif phase == "LANDED":
        new_data["altitude"] = 0
        new_data["vertical_speed"] = 0
        new_data["ground_speed"] = 0
        new_data["airspeed"] = 0
        new_data["mode"] = "Manual"
        
        if time.time() - state.get("landed_time", time.time()) > 5:
            new_data["battery_level"] = 100.0 
            
            if new_data["battery_level"] >= LOW_BATTERY_THRESHOLD:
                print("--- 🔄  Misi Selesai. Ganti Baterai & Mengulang Misi Baru ---")
                state["phase"] = "CLIMB"
                new_data["mission_id"] = new_data.get("mission_id", "M001") + "_R"
            else:
                print("--- ⛔ Baterai < 25%. MISI DIBATALKAN. ---")
                state["phase"] = "LANDED" 
    
    new_data["gps_alt"] = new_data["altitude"] + random.uniform(-2, 2)
    new_data["lidar_altitude"] = new_data["altitude"] + random.uniform(-0.5, 0.5)

    if state["phase"] != "LANDED":
        heading_change = random.uniform(-5, 5)
        new_data["heading"] = (new_data.get("heading", 90.0) + heading_change) % 360
        new_data["yaw"] = new_data["heading"]
        
        distance = new_data["ground_speed"] / 111000.0
        new_data["gps_lat"] = new_data.get("gps_lat", -7.27) + np.sin(np.deg2rad(new_data["heading"])) * distance
        new_data["gps_lon"] = new_data.get("gps_lon", 112.74) + np.cos(np.deg2rad(new_data["heading"])) * distance
        
        new_data["pitch"] = random.uniform(-10, 10)
        new_data["roll"] = random.uniform(-20, 20)
    else:
        new_data["pitch"] = 0
        new_data["roll"] = 0

    new_data["accel_x"] = random.uniform(-0.5, 0.5)
    new_data["accel_y"] = random.uniform(-0.5, 0.5)
    new_data["accel_z"] = random.uniform(-0.5, 0.5)
    new_data["gyro_x"] = random.uniform(-0.02, 0.02)
    new_data["gyro_y"] = random.uniform(-0.02, 0.02)
    new_data["gyro_z"] = random.uniform(-0.02, 0.02)
    
    for i in range(1, 5):
        if state["phase"] != "LANDED":
            new_data[f"motor_rpm_{i}"] = random.uniform(3000, 8000)
            new_data[f"motor_temp_{i}"] = random.uniform(40, 90)
        else:
            new_data[f"motor_rpm_{i}"] = 0
            new_data[f"motor_temp_{i}"] = max(25, new_data.get(f"motor_temp_{i}", 25) - 0.1)
    
    new_data["throttle_position"] = random.uniform(40, 100) if state["phase"] != "LANDED" else 0
    new_data["payload_weight"] = random.choice([0.0, 2.5, 5.0, 10.0])
    new_data["obstacle_distance"] = random.uniform(5, 200)
    new_data["sat_count"] = random.randint(5, 12)
    new_data["gps_fix_type"] = random.choice([2, 3])
    new_data["link_quality"] = random.uniform(40, 100)
    new_data["signal_strength"] = random.uniform(-110, -50)
    
    if state["phase"] == "LANDED":
        new_data["system_status"] = "Landed"
    elif new_data["battery_level"] < 15:
        new_data["system_status"] = "Warning"
    elif new_data["battery_level"] < 7:
        new_data["system_status"] = "Error"
    else:
        new_data["system_status"] = "Normal"
    
    if not new_data.get("event"): 
        new_data["event"] = ""

    # === 💣 INJEKSI ANOMALI DIAM-DIAM ===
    # 
    # Beri 20% kemungkinan anomali terjadi HANYA JIKA sedang terbang
    if state["phase"] != "LANDED" and random.random() < 0.05: # 5% chance
        
        # [ PERUBAHAN DI SINI ]
        # Kita membuat 'battery_drop' lebih jarang terjadi (probabilitas 1/5 atau 20%)
        # 'motor_fail' dan 'sensor_glitch' kini lebih sering (probabilitas 2/5 atau 40% masing-masing)
        
        if new_data["battery_level"] < LOW_BATTERY_THRESHOLD + 5:
            # Jika baterai kritis, jangan injeksi anomali baterai
            anomaly_type = random.choice(["motor_fail", "sensor_glitch"])
        else:
            # Jika baterai normal, gunakan daftar probabilitas yang baru
            anomaly_type = random.choice([
                "motor_fail", "sensor_glitch", # Sering
                "motor_fail", "sensor_glitch", # Sering
                "battery_drop"                 # Jarang (Hanya 1 dari 5)
            ])
        # [ AKHIR PERUBAHAN ]

        
        if anomaly_type == "motor_fail":
            motor_num = random.randint(1, 4)
            new_data[f"motor_rpm_{motor_num}"] = 0  
            new_data[f"motor_temp_{motor_num}"] = 150.0 
            new_data["event"] = f"Motor {motor_num} Failure"

        elif anomaly_type == "sensor_glitch":
            new_data["altitude"] += random.uniform(50, 150)
            new_data["event"] = "Altitude Sensor Glitch"

        elif anomaly_type == "battery_drop":
            new_data["battery_level"] = max(5, new_data["battery_level"] - random.uniform(10, 20))
            new_data["event"] = "Sudden Battery Drop"
            
    # ========================================

    new_data["mission_id"] = new_data.get("mission_id", "M001")
    new_data["waypoint_id"] = int(new_data.get("waypoint_id", 0) + random.choice([0,0,0,1])) % 10
    
    return new_data, state


def main():
    """Loop utama produser data telemetri"""
    print("🚁 UAV Telemetry Producer dimulai...")
    print("=" * 50)
    print(f"Database target: {DB_PATH}")
    print(f"CSV sumber: {CSV_PATH}")
    
    columns = init_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # --- PERBAIKAN DATABASE LOCK (BARU) ---
    # Aktifkan mode WAL (Write-Ahead Logging)
    # Ini mengizinkan 'app.py' (pembaca) berjalan TANPA diblokir oleh 'uav_producer.py' (penulis)
    try:
        cursor.execute("PRAGMA journal_mode=WAL;")
        print("✓ Mode WAL (Write-Ahead Logging) diaktifkan untuk mengatasi database lock.")
    except Exception as e:
        print(f"⚠ Peringatan: Gagal mengaktifkan mode WAL. {e}")
    # -------------------------------
    
    # PANGGILAN PERTAMA (DAN SATU-SATUNYA)
    template = get_last_row_template(cursor, columns)
    
    # === Setting Misi 5000m ===
    cruise_time_seconds = random.randint(120, 180) # Acak 2-3 menit (120-180 detik)
    flight_state = {
        "phase": "CLIMB",
        "target_altitude": 5000.0,           # Target 5000 meter
        "climb_rate": 30.0,                  # Naik 30 m/s
        "descend_rate": -25.0,               # Turun 25 m/s
        "cruise_duration_seconds": cruise_time_seconds, 
        "cruise_start_time": None
    }
    
    # === LOGIKA YANG DIPERBAIKI ===
    current_altitude = template.get("altitude", 0)
    
    if current_altitude <= 0:
        # Kita di darat. Cek apakah ini DB baru atau misi lama.
        if template.get("battery_level", 0) < 100:
            # Ini misi lama (baterai tidak 100%). Reset baterai.
            template["battery_level"] = 100.0 
            print("Memulai misi baru dari darat dengan baterai penuh (Reset Baterai).")
        else:
            # Ini DB baru (baterai sudah 100%). Tidak perlu 'print'
            # (Pesan "Database kosong" sudah dicetak oleh get_last_row_template)
            pass 
            
        flight_state["phase"] = "CLIMB"
        
    elif current_altitude < flight_state["target_altitude"]:
         # Melanjutkan misi yang sedang naik
         flight_state["phase"] = "CLIMB"
    else:
        # Melanjutkan misi yang sedang cruise
        flight_state["phase"] = "CRUISE"
        flight_state["cruise_start_time"] = time.time()
    # ===============================

    print(f"✓ Templat data dimuat (timestamp: {template.get('timestamp', 'N/A')})")
    print(f"✈️  Memulai Misi: Target 5000m, Cruise {cruise_time_seconds} detik. Fase Awal: {flight_state['phase']}")
    print("\n🔄 Memulai loop produser (Ctrl+C untuk berhenti)...")
    print("=" * 50)
    
    try:
        while True:
            new_data, flight_state = generate_new_telemetry(template, flight_state)
            
            values = []
            for col in columns:
                values.append(new_data.get(col))

            placeholders = ','.join(['?' for _ in columns])
            insert_sql = f"INSERT INTO telemetry ({','.join(columns)}) VALUES ({placeholders})"
            
            cursor.execute(insert_sql, values)
            conn.commit()
            
            template = new_data
            
            timestamp_str = new_data.get("dt", "N/A")
            altitude = new_data.get("altitude", 0)
            battery = new_data.get("battery_level", 0)
            status = new_data.get("system_status", "Unknown")
            phase = flight_state["phase"]
            
            print(f"[{timestamp_str}] ✓ Fase: {phase} | Alt: {altitude:.1f}m | Battery: {battery:.1f}% | Status: {status}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Produser dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        conn.close()
        print("✓ Koneksi database ditutup")

if __name__ == "__main__":
    main()