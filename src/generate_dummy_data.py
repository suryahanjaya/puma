# generate_dummy_data.py
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
import os

# Feature yang diharapkan untuk anomaly detection
DESIRED_FEATURES = [
    "altitude", "gps_alt",
    "ground_speed", "airspeed", "vertical_speed",
    "heading", "pitch", "roll", "yaw",
    "accel_x", "accel_y", "accel_z",
    "gyro_x", "gyro_y", "gyro_z",
    "battery_level", "battery_voltage", "battery_current", "temperature_battery",
    "motor_rpm_1", "motor_rpm_2", "motor_rpm_3", "motor_rpm_4",
    "motor_temp_1", "motor_temp_2", "motor_temp_3", "motor_temp_4",
    "throttle_position", "payload_weight", "lidar_altitude", "obstacle_distance",
    "sat_count", "gps_fix_type", "link_quality", "signal_strength",
    "mode", "system_status"
]

def generate_data_v3(total_cycles=10, data_per_cycle=600, anomaly_ratio=0.20, out_path="data/telemetry_data.csv"):
    """
    Generate UAV telemetry data dengan pola yang sama seperti uav_producer.py
    untuk N cycle lengkap (CLIMB -> CRUISE -> DESCEND -> LANDED)
    
    Parameters:
    - total_cycles: Jumlah cycle penerbangan lengkap
    - data_per_cycle: Jumlah data points (baris) per cycle
    - anomaly_ratio: Rasio anomali dari total data (0.20 = 20%)
    - out_path: Path output file CSV
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Base time mulai dari sekarang
    base_time = datetime.now()
    rows = []
    
    # Parameter misi (sama seperti uav_producer)
    target_altitude = 5000.0
    
    # Hitung durasi masing-masing fase berdasarkan data_per_cycle
    # Distribusi: CLIMB 30%, CRUISE 40%, DESCEND 25%, LANDED 5%
    climb_data_points = int(data_per_cycle * 0.30)
    cruise_data_points = int(data_per_cycle * 0.40)
    descend_data_points = int(data_per_cycle * 0.25)
    landed_data_points = int(data_per_cycle * 0.05)
    
    # Hitung rates berdasarkan durasi
    climb_rate = target_altitude / climb_data_points  # m per data point
    descend_rate = -target_altitude / descend_data_points  # m per data point
    
    # Hitung target anomali
    total_data_points = total_cycles * data_per_cycle
    target_anomalies = int(total_data_points * anomaly_ratio)
    
    print(f"🚁 Generating {total_cycles} complete flight cycles...")
    print(f"Target Altitude: {target_altitude}m | Data per cycle: {data_per_cycle}")
    print(f"Phase distribution: CLIMB({climb_data_points}), CRUISE({cruise_data_points}), DESCEND({descend_data_points}), LANDED({landed_data_points})")
    print(f"🎯 Target anomalies: {target_anomalies} ({anomaly_ratio*100}% of {total_data_points} total data)")
    print("=" * 70)
    
    # Counter untuk anomali
    anomaly_count = 0
    
    # Jenis anomali yang lebih variatif
    anomaly_types = [
        "motor_fail", "sensor_glitch", "battery_drop", 
        "communication_loss", "gps_drift", "imu_spike",
        "overheating", "stall_warning", "vibration_high"
    ]
    
    for cycle in range(1, total_cycles + 1):
        # State untuk cycle ini
        flight_state = {
            "phase": "CLIMB",
            "target_altitude": target_altitude,
            "climb_rate": climb_rate,
            "descend_rate": descend_rate,
            "current_cycle": cycle,
            "phase_counter": 0,
            "total_phase_points": climb_data_points
        }
        
        # Data template untuk cycle ini
        template = {
            "timestamp": int(time.time()),
            "dt": base_time.strftime("%Y/%m/%d %H:%M:%S"),
            "date": base_time.strftime("%Y/%m/%d"),
            "altitude": 0.0, "gps_alt": 0.0,
            "gps_lat": -7.27 + (cycle-1) * 0.02,  # Geser sedikit setiap cycle
            "gps_lon": 112.74 + (cycle-1) * 0.02,
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
            "mission_id": f"M{cycle:03d}", "waypoint_id": 0, "event": ""
        }
        
        current_data = template.copy()
        cycle_start_time = base_time + timedelta(minutes=(cycle-1)*10)  # Setiap cycle mulai 10 menit setelah sebelumnya
        
        print(f"\n🔄 Starting Cycle {cycle}/{total_cycles} - Mission {current_data['mission_id']}")
        
        for data_point in range(data_per_cycle):
            current_time = cycle_start_time + timedelta(seconds=data_point)
            current_data["timestamp"] = int(current_time.timestamp())
            current_data["dt"] = current_time.strftime("%Y/%m/%d %H:%M:%S")
            current_data["date"] = current_time.strftime("%Y/%m/%d")
            
            phase = flight_state["phase"]
            flight_state["phase_counter"] += 1
            
            # === FASE CLIMB ===
            if phase == "CLIMB":
                altitude_change = flight_state["climb_rate"] + random.uniform(-0.5, 0.5)
                current_data["altitude"] = max(0, current_data.get("altitude", 0) + altitude_change)
                current_data["vertical_speed"] = altitude_change
                current_data["mode"] = "Auto"
                current_data["system_status"] = "Normal"
                
                # Check phase transition
                if flight_state["phase_counter"] >= flight_state["total_phase_points"]:
                    current_data["altitude"] = flight_state["target_altitude"]
                    flight_state["phase"] = "CRUISE"
                    flight_state["phase_counter"] = 0
                    flight_state["total_phase_points"] = cruise_data_points
                    current_data["vertical_speed"] = 0
                    print(f"   ↥ CLIMB → CRUISE at {current_data['altitude']:.1f}m")
            
            # === FASE CRUISE ===
            elif phase == "CRUISE":
                altitude_change = random.uniform(-1.5, 1.5)
                current_data["altitude"] = flight_state["target_altitude"] + altitude_change
                current_data["vertical_speed"] = altitude_change
                current_data["mode"] = "Auto"
                current_data["system_status"] = "Normal"
                
                if flight_state["phase_counter"] >= flight_state["total_phase_points"]:
                    flight_state["phase"] = "DESCEND"
                    flight_state["phase_counter"] = 0
                    flight_state["total_phase_points"] = descend_data_points
                    print(f"   → CRUISE → DESCEND")
            
            # === FASE DESCEND ===
            elif phase == "DESCEND":
                altitude_change = flight_state["descend_rate"] + random.uniform(-0.5, 0.5)
                current_data["altitude"] = max(0, current_data.get("altitude", 0) + altitude_change)
                current_data["vertical_speed"] = altitude_change
                current_data["mode"] = "RTL"
                
                # System status based on battery
                current_battery = current_data.get("battery_level", 0)
                if current_battery < 15:
                    current_data["system_status"] = "Warning"
                elif current_battery < 7:
                    current_data["system_status"] = "Error"
                else:
                    current_data["system_status"] = "Normal"
                
                if flight_state["phase_counter"] >= flight_state["total_phase_points"]:
                    current_data["altitude"] = 0
                    flight_state["phase"] = "LANDED"
                    flight_state["phase_counter"] = 0
                    flight_state["total_phase_points"] = landed_data_points
                    current_data["vertical_speed"] = 0
                    print(f"   ↧ DESCEND → LANDED")
            
            # === FASE LANDED ===
            elif phase == "LANDED":
                current_data["altitude"] = 0
                current_data["vertical_speed"] = 0
                current_data["ground_speed"] = 0
                current_data["airspeed"] = 0
                current_data["mode"] = "Manual"
                current_data["system_status"] = "Landed"
                
                if flight_state["phase_counter"] >= flight_state["total_phase_points"]:
                    print(f"   ✓ Cycle {cycle} COMPLETED")
                    break  # Pindah ke cycle berikutnya
            
            # === UPDATE SEMUA FEATURE YANG DIINGINKAN ===
            
            # Kecepatan (hanya saat terbang)
            if phase != "LANDED":
                current_data["ground_speed"] = random.uniform(10, 70)
                current_data["airspeed"] = current_data["ground_speed"] + random.uniform(-2, 2)
            else:
                current_data["ground_speed"] = 0
                current_data["airspeed"] = 0
            
            # Sensor altitude
            current_data["gps_alt"] = current_data["altitude"] + random.uniform(-2, 2)
            current_data["lidar_altitude"] = current_data["altitude"] + random.uniform(-0.5, 0.5)
            
            # Posisi dan orientasi (hanya saat terbang)
            if phase != "LANDED":
                heading_change = random.uniform(-5, 5)
                current_data["heading"] = (current_data.get("heading", 90.0) + heading_change) % 360
                current_data["yaw"] = current_data["heading"]
                
                # Gerakkan posisi GPS
                distance = current_data["ground_speed"] / 111000.0
                current_data["gps_lat"] += np.sin(np.deg2rad(current_data["heading"])) * distance
                current_data["gps_lon"] += np.cos(np.deg2rad(current_data["heading"])) * distance
                
                current_data["pitch"] = random.uniform(-10, 10)
                current_data["roll"] = random.uniform(-20, 20)
            else:
                current_data["pitch"] = 0
                current_data["roll"] = 0
            
            # Sensor IMU
            current_data["accel_x"] = random.uniform(-0.5, 0.5)
            current_data["accel_y"] = random.uniform(-0.5, 0.5)
            current_data["accel_z"] = random.uniform(-0.5, 0.5)
            current_data["gyro_x"] = random.uniform(-0.02, 0.02)
            current_data["gyro_y"] = random.uniform(-0.02, 0.02)
            current_data["gyro_z"] = random.uniform(-0.02, 0.02)
            
            # Baterai (berkurang hanya saat terbang)
            if phase != "LANDED":
                battery_decrease = random.uniform(0.05, 0.10)
                current_data["battery_level"] = max(5, current_data.get("battery_level", 100.0) - battery_decrease)
            
            current_data["battery_voltage"] = 14.8 * (current_data["battery_level"] / 100) + random.uniform(-0.1, 0.1)
            current_data["battery_current"] = random.uniform(5, 25) if phase != "LANDED" else 0
            current_data["temperature_battery"] = random.uniform(20, 45)
            
            # Motor (hanya saat terbang)
            for i in range(1, 5):
                if phase != "LANDED":
                    current_data[f"motor_rpm_{i}"] = random.uniform(3000, 8000)
                    current_data[f"motor_temp_{i}"] = random.uniform(40, 90)
                else:
                    current_data[f"motor_rpm_{i}"] = 0
                    current_data[f"motor_temp_{i}"] = max(25, current_data.get(f"motor_temp_{i}", 25) - 0.1)
            
            current_data["throttle_position"] = random.uniform(40, 100) if phase != "LANDED" else 0
            current_data["payload_weight"] = random.choice([0.0, 2.5, 5.0, 10.0])
            current_data["obstacle_distance"] = random.uniform(5, 200)
            current_data["sat_count"] = random.randint(5, 12)
            current_data["gps_fix_type"] = random.choice([2, 3])
            current_data["link_quality"] = random.uniform(40, 100)
            current_data["signal_strength"] = random.uniform(-110, -50)
            
            # Waypoint progress
            current_data["waypoint_id"] = (current_data.get("waypoint_id", 0) + 1) % 20
            
            # === INJEKSI ANOMALI 20% DARI TOTAL DATA ===
            current_data["event"] = ""  # Reset event
            
            # Hitung probabilitas anomali untuk mencapai target 20%
            remaining_data = total_data_points - len(rows)
            remaining_anomalies = target_anomalies - anomaly_count
            
            # Probabilitas dinamis untuk mencapai tepat 20%
            if phase != "LANDED" and remaining_anomalies > 0:
                current_probability = remaining_anomalies / remaining_data if remaining_data > 0 else 0
                
                # Tambahkan faktor random untuk distribusi yang natural
                if random.random() < current_probability * 1.2:  # 1.2 factor untuk kompensasi
                    anomaly_type = random.choice(anomaly_types)
                    anomaly_count += 1
                    
                    if anomaly_type == "motor_fail":
                        motor_num = random.randint(1, 4)
                        current_data[f"motor_rpm_{motor_num}"] = 0
                        current_data[f"motor_temp_{motor_num}"] = 150.0
                        current_data["event"] = f"Motor {motor_num} Failure"
                        current_data["system_status"] = "Error"

                    elif anomaly_type == "sensor_glitch":
                        current_data["altitude"] += random.uniform(100, 300)
                        current_data["gps_alt"] = current_data["altitude"] + random.uniform(-50, 50)
                        current_data["event"] = "Altitude Sensor Glitch"
                        current_data["system_status"] = "Warning"

                    elif anomaly_type == "battery_drop":
                        current_data["battery_level"] = max(5, current_data["battery_level"] - random.uniform(20, 40))
                        current_data["battery_voltage"] = 14.8 * (current_data["battery_level"] / 100) - random.uniform(1, 3)
                        current_data["event"] = "Sudden Battery Drop"
                        current_data["system_status"] = "Warning"

                    elif anomaly_type == "communication_loss":
                        current_data["link_quality"] = random.uniform(0, 10)
                        current_data["signal_strength"] = random.uniform(-120, -100)
                        current_data["sat_count"] = random.randint(0, 3)
                        current_data["event"] = "Communication Loss"
                        current_data["system_status"] = "Error"

                    elif anomaly_type == "gps_drift":
                        current_data["gps_lat"] += random.uniform(-0.1, 0.1)
                        current_data["gps_lon"] += random.uniform(-0.1, 0.1)
                        current_data["gps_fix_type"] = 1
                        current_data["event"] = "GPS Drift"
                        current_data["system_status"] = "Warning"

                    elif anomaly_type == "imu_spike":
                        current_data["accel_x"] = random.uniform(-10, 10)
                        current_data["accel_y"] = random.uniform(-10, 10)
                        current_data["accel_z"] = random.uniform(-10, 10)
                        current_data["gyro_x"] = random.uniform(-1, 1)
                        current_data["gyro_y"] = random.uniform(-1, 1)
                        current_data["gyro_z"] = random.uniform(-1, 1)
                        current_data["event"] = "IMU Sensor Spike"
                        current_data["system_status"] = "Warning"

                    elif anomaly_type == "overheating":
                        for i in range(1, 5):
                            current_data[f"motor_temp_{i}"] += random.uniform(30, 60)
                        current_data["temperature_battery"] += random.uniform(20, 40)
                        current_data["event"] = "System Overheating"
                        current_data["system_status"] = "Error"

                    elif anomaly_type == "stall_warning":
                        current_data["airspeed"] = random.uniform(0, 5)
                        current_data["ground_speed"] = random.uniform(0, 5)
                        current_data["vertical_speed"] = random.uniform(-10, -5)
                        current_data["event"] = "Stall Warning"
                        current_data["system_status"] = "Warning"

                    elif anomaly_type == "vibration_high":
                        for i in range(1, 5):
                            current_data[f"motor_rpm_{i}"] *= random.uniform(1.2, 1.5)
                        current_data["event"] = "High Vibration"
                        current_data["system_status"] = "Warning"
                    
                    # Progress indicator untuk anomali
                    if anomaly_count % 50 == 0 or anomaly_count <= 10:
                        print(f"   ⚠️  ANOMALY #{anomaly_count}: {current_data['event']} at cycle {cycle}, point {data_point}")
            
            # Tambahkan data ke list
            rows.append(current_data.copy())
    
    # Convert ke DataFrame
    df = pd.DataFrame(rows)
    
    # Pastikan semua DESIRED_FEATURES ada dalam DataFrame
    for feature in DESIRED_FEATURES:
        if feature not in df.columns:
            print(f"⚠️  Warning: {feature} not found in generated data, adding with default values")
            if feature in ["gps_fix_type", "sat_count"]:
                df[feature] = 3  # Default integer
            elif feature in ["mode", "system_status"]:
                df[feature] = "Normal"  # Default string
            else:
                df[feature] = 0.0  # Default float
    
    # Pastikan tipe data konsisten untuk numeric features
    numeric_features = [f for f in DESIRED_FEATURES if f not in ["mode", "system_status"]]
    
    for col in numeric_features:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Simpan ke CSV
    df.to_csv(out_path, index=False)
    
    # Statistics
    total_rows = len(df)
    expected_rows = total_cycles * data_per_cycle
    actual_anomaly_ratio = anomaly_count / total_rows
    
    print("\n" + "=" * 70)
    print("📊 GENERATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully generated {total_rows} rows")
    print(f"🎯 Target: {total_cycles} cycles × {data_per_cycle} data/cycle = {expected_rows} rows")
    print(f"📈 Actual vs Target: {total_rows} / {expected_rows} ({total_rows/expected_rows*100:.1f}%)")
    print(f"📁 Saved to: {out_path}")
    print(f"⏰ Time range: {df['dt'].min()} to {df['dt'].max()}")
    print(f"🔄 Total cycles completed: {total_cycles}")
    print(f"📈 Max altitude: {df['altitude'].max():.1f}m")
    print(f"🔋 Final battery: {df['battery_level'].iloc[-1]:.1f}%")
    print(f"🔍 Features generated: {len([f for f in DESIRED_FEATURES if f in df.columns])}/{len(DESIRED_FEATURES)}")
    print(f"🚨 ABNORMALITIES SUMMARY:")
    print(f"   • Target anomalies: {target_anomalies} ({anomaly_ratio*100}%)")
    print(f"   • Actual anomalies: {anomaly_count} ({actual_anomaly_ratio*100:.1f}%)")
    print(f"   • Anomaly types used: {len(anomaly_types)}")
    print(f"   • Accuracy: {actual_anomaly_ratio/anomaly_ratio*100:.1f}% of target")
    
    # Tampilkan distribusi anomali per jenis
    if 'event' in df.columns:
        anomaly_distribution = df[df['event'] != '']['event'].value_counts()
        print(f"   • Distribution: {anomaly_distribution.to_dict()}")
    
    return df

if __name__ == "__main__":
    # Generate 30 cycle lengkap dengan 600 data per cycle = 18,000 baris total
    # Dengan 20% anomali = 3,600 data anomali
    df = generate_data_v3(
        total_cycles=30, 
        data_per_cycle=600,
        anomaly_ratio=0.20,  # 20% anomali
        out_path="data/telemetry_data.csv"
    )