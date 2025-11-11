# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sqlite3
import json
import time
import os
import plotly.graph_objects as go

# --- Konfigurasi Path ---
DB_PATH = "data/uav_telemetry.db"
MODEL_PATH = "models/lof_novelty.joblib"
SCALER_PATH = "models/data_scaler.joblib"
FEATURES_PATH = "data/feature_names.json"

# --- 1. Load Aset (Model, Scaler, Fitur) ---
# Menggunakan cache Streamlit agar model tidak di-load ulang setiap refresh
@st.cache_resource
def load_assets():
    """Memuat model, scaler, dan daftar fitur."""
    print("--- 🚀 Memuat aset model... ---")
    if not os.path.exists(MODEL_PATH):
        st.error(f"Error: Model tidak ditemukan di {MODEL_PATH}")
        return None, None, None
    if not os.path.exists(SCALER_PATH):
        st.error(f"Error: Scaler tidak ditemukan di {SCALER_PATH}")
        return None, None, None
    if not os.path.exists(FEATURES_PATH):
        st.error(f"Error: Daftar Fitur tidak ditemukan di {FEATURES_PATH}")
        return None, None, None
        
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        with open(FEATURES_PATH, 'r') as f:
            feature_names = json.load(f)
        
        print(f"--- ✅ Aset berhasil dimuat. {len(feature_names)} fitur. ---")
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"Gagal memuat aset: {e}")
        return None, None, None

# --- 2. Logika Feature Engineering (SAMA DENGAN NOTEBOOK) ---
def feature_engineering(df):
    """
    Membuat fitur-fitur baru dari data mentah.
    Harus identik dengan train_model_adaptive.ipynb
    """
    df_eng = df.copy()

    # 1. Agregat Motor
    motor_rpm_cols = ['motor_rpm_1', 'motor_rpm_2', 'motor_rpm_3', 'motor_rpm_4']
    if all(c in df_eng.columns for c in motor_rpm_cols):
        df_eng['motor_rpm_std'] = df_eng[motor_rpm_cols].std(axis=1)
        df_eng['motor_rpm_mean'] = df_eng[motor_rpm_cols].mean(axis=1)

    motor_temp_cols = ['motor_temp_1', 'motor_temp_2', 'motor_temp_3', 'motor_temp_4']
    if all(c in df_eng.columns for c in motor_temp_cols):
        df_eng['motor_temp_std'] = df_eng[motor_temp_cols].std(axis=1)

    # 2. Sensor Disagreement
    alt_cols = ['altitude', 'gps_alt', 'lidar_altitude']
    if all(c in df_eng.columns for c in alt_cols):
        df_eng['alt_disagreement_std'] = df_eng[alt_cols].std(axis=1)

    # 3. Power System
    if 'battery_voltage' in df_eng.columns and 'battery_current' in df_eng.columns:
        df_eng['power_draw'] = df_eng['battery_voltage'] * df_eng['battery_current']

    # 4. Rolling Statistics (Butuh data historis, makanya kita ambil > 1 baris)
    # Urutkan berdasarkan timestamp untuk memastikan rolling window benar
    df_eng = df_eng.sort_values(by='timestamp', ascending=True)
    
    if 'accel_z' in df_eng.columns:
        df_eng['roll_accel_z_std'] = df_eng['accel_z'].rolling(window=5, min_periods=1).std()

    if 'gyro_x' in df_eng.columns:
        df_eng['roll_gyro_x_std'] = df_eng['gyro_x'].rolling(window=5, min_periods=1).std()

    # Kembalikan ke urutan asli (terbaru di atas)
    df_eng = df_eng.sort_values(by='timestamp', ascending=False)
    
    # Isi NaN yang muncul dari rolling std (di awal data)
    df_eng = df_eng.fillna(0)
    
    return df_eng

# --- 3. Fungsi Prediksi ---
def predict_anomalies(df, model, scaler, feature_names):
    """Melakukan feature engineering, scaling, dan prediksi."""
    if df.empty:
        return df

    # 1. Lakukan Feature Engineering
    df_engineered = feature_engineering(df)
    
    # 2. Pastikan semua kolom ada
    missing_cols = set(feature_names) - set(df_engineered.columns)
    if missing_cols:
        st.warning(f"Fitur hilang saat prediksi: {missing_cols}")
        for col in missing_cols:
            df_engineered[col] = 0 # Tambahkan kolom kosong jika hilang

    # 3. Jaga urutan kolom tetap sama
    df_aligned = df_engineered[feature_names]

    # 4. Scaling
    df_scaled = scaler.transform(df_aligned)
    
    # 5. Prediksi (Gunakan .predict() untuk label, .decision_function untuk skor)
    # .predict() -> 1 = inlier (normal), -1 = outlier (anomali)
    predictions = model.predict(df_scaled)
    
    # .decision_function() -> skor mentah (kita balik agar TINGGI = anomali)
    scores = -model.decision_function(df_scaled)
    
    # Tambahkan hasil ke DataFrame asli
    df['is_anomaly'] = (predictions == -1).astype(int)
    df['anomaly_score'] = scores
    
    return df

# --- 4. Fungsi Ambil Data ---
def fetch_latest_data(conn, limit=100):
    """Mengambil N baris data terbaru dari database."""
    try:
        query = f"SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        return df
    except pd.errors.DatabaseError as e:
        if "database is locked" in str(e):
            st.error("Database terkunci. Pastikan uav_producer.py berjalan.")
            return pd.DataFrame()
        else:
            raise e
    except Exception as e:
        st.warning(f"Gagal mengambil data: {e}")
        return pd.DataFrame()


# --- 5. Halaman Utama Dashboard ---
def run_dashboard():
    st.set_page_config(page_title="UAV Anomaly Detection", layout="wide")
    st.title("🛰️ UAV Real-Time Anomaly Detection")
    st.markdown(f"Memantau database: `{DB_PATH}` | Model: `{MODEL_PATH}`")

    history_limit = st.number_input(
        "Jumlah Data Terakhir yang Ditampilkan:", 
        min_value=50, 
        max_value=5000, 
        value=150, # Nilai default
        step=50
    )

    # Load aset
    model, scaler, feature_names = load_assets()
    if model is None:
        st.error("Gagal memuat aset model. Dashboard tidak dapat berjalan.")
        return

    # Siapkan placeholder untuk update real-time
    placeholder = st.empty()

    # Loop utama dashboard
    while True:
        try:
            # Gunakan mode read-only (ro) agar tidak bentrok dengan producer
            db_uri = f'file:{DB_PATH}?mode=ro'
            conn = sqlite3.connect(db_uri, uri=True, check_same_thread=False)
            
            raw_data = fetch_latest_data(conn, limit=history_limit)
            conn.close()

            if raw_data.empty:
                with placeholder.container():
                    st.warning("Menunggu data dari uav_producer.py...")
                time.sleep(2)
                continue

            # Lakukan prediksi
            df_results = predict_anomalies(raw_data, model, scaler, feature_names)

            # Ambil data T Terbaru
            latest_data = df_results.iloc[0]
            
            with placeholder.container():
                
                # --- KPI (Key Performance Indicators) ---
                st.header("Status Terbaru")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                # Tampilkan status anomali
                if latest_data['is_anomaly'] == 1:
                    col1.metric("System Status", "🔴 ANOMALY", "Deteksi Model")
                else:
                    col1.metric("System Status", "🟢 NORMAL", "Deteksi Model")

                col2.metric("Timestamp", latest_data['dt'].split(' ')[-1])
                col3.metric("Altitude", f"{latest_data['altitude']:.1f} m")
                col4.metric("Battery Level", f"{latest_data['battery_level']:.1f} %")
                col5.metric("Flight Mode", latest_data['mode'])
                
                st.markdown("---")
                
                # --- Grafik ---
                st.header(f"Grafik Real-Time ({history_limit} Data Terakhir)")
                
                # Balik urutan data agar waktu berjalan dari kiri ke kanan
                df_plot = df_results.iloc[::-1].reset_index(drop=True)

                col_a, col_b = st.columns(2)
                
                with col_a:
                    # Grafik 1: Skor Anomali
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(
                        x=df_plot['dt'], 
                        y=df_plot['anomaly_score'], 
                        name='Anomaly Score',
                        line=dict(color='orange')
                    ))
                    # Tandai data yang diprediksi sebagai anomali
                    anomalies = df_plot[df_plot['is_anomaly'] == 1]
                    fig1.add_trace(go.Scatter(
                        x=anomalies['dt'], 
                        y=anomalies['anomaly_score'], 
                        name='Anomaly Detected',
                        mode='markers',
                        marker=dict(color='red', size=8, symbol='x')
                    ))
                    fig1.update_layout(title='Skor Anomali (Tinggi = Anomali)', yaxis_title='Score')
                    st.plotly_chart(fig1, width='stretch')

                with col_b:
                    # Grafik 2: Metrik Kunci
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(x=df_plot['dt'], y=df_plot['altitude'], name='Altitude (m)'))
                    fig2.add_trace(go.Scatter(x=df_plot['dt'], y=df_plot['battery_level'], name='Battery (%)', yaxis='y2'))
                    fig2.update_layout(
                        title='Metrik Penerbangan',
                        yaxis=dict(title='Altitude (m)'),
                        yaxis2=dict(title='Battery (%)', overlaying='y', side='right')
                    )
                    st.plotly_chart(fig2, width='stretch')

                # --- Tabel Data ---
                st.header("Data Mentah Terbaru")
                st.dataframe(df_results[[
                    'dt', 'is_anomaly', 'anomaly_score', 'altitude', 
                    'battery_level', 'mode', 'system_status', 'event' # Tampilkan 'event' untuk perbandingan
                ]].head(15))

        except Exception as e:
            st.error(f"Terjadi error pada dashboard loop: {e}")
            import traceback
            st.code(traceback.format_exc())

        # Refresh rate
        time.sleep(1.5) # Refresh setiap 1.5 detik

if __name__ == "__main__":
    run_dashboard()