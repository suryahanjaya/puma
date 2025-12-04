"""
Flask API Backend for PUMA Dashboard
Provides REST API endpoints to serve UAV telemetry data
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import sqlite3
import pandas as pd
import numpy as np
import joblib
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend

# Configuration
DB_PATH = "data/uav_telemetry.db"
MODEL_PATH = "models/lof_novelty.joblib"
SCALER_PATH = "models/data_scaler.joblib"
FEATURES_PATH = "data/feature_names.json"

# Load ML assets
print("Loading ML assets...")
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
with open(FEATURES_PATH, 'r') as f:
    feature_names = json.load(f)
print(f"✓ Loaded model with {len(feature_names)} features")


def feature_engineering(df):
    """Feature engineering - must match training pipeline"""
    df_eng = df.copy()

    # Motor aggregations
    motor_rpm_cols = ['motor_rpm_1', 'motor_rpm_2', 'motor_rpm_3', 'motor_rpm_4']
    if all(c in df_eng.columns for c in motor_rpm_cols):
        df_eng['motor_rpm_std'] = df_eng[motor_rpm_cols].std(axis=1)
        df_eng['motor_rpm_mean'] = df_eng[motor_rpm_cols].mean(axis=1)

    motor_temp_cols = ['motor_temp_1', 'motor_temp_2', 'motor_temp_3', 'motor_temp_4']
    if all(c in df_eng.columns for c in motor_temp_cols):
        df_eng['motor_temp_std'] = df_eng[motor_temp_cols].std(axis=1)

    # Sensor disagreement
    alt_cols = ['altitude', 'gps_alt', 'lidar_altitude']
    if all(c in df_eng.columns for c in alt_cols):
        df_eng['alt_disagreement_std'] = df_eng[alt_cols].std(axis=1)

    # Power system
    if 'battery_voltage' in df_eng.columns and 'battery_current' in df_eng.columns:
        df_eng['power_draw'] = df_eng['battery_voltage'] * df_eng['battery_current']

    # Rolling statistics
    df_eng = df_eng.sort_values(by='timestamp', ascending=True)
    
    if 'accel_z' in df_eng.columns:
        df_eng['roll_accel_z_std'] = df_eng['accel_z'].rolling(window=5, min_periods=1).std()

    if 'gyro_x' in df_eng.columns:
        df_eng['roll_gyro_x_std'] = df_eng['gyro_x'].rolling(window=5, min_periods=1).std()

    df_eng = df_eng.sort_values(by='timestamp', ascending=False)
    df_eng = df_eng.fillna(0)
    
    return df_eng


def predict_anomalies(df):
    """Perform anomaly detection on telemetry data"""
    if df.empty:
        return df

    # Feature engineering
    df_engineered = feature_engineering(df)
    
    # Ensure all features exist
    missing_cols = set(feature_names) - set(df_engineered.columns)
    for col in missing_cols:
        df_engineered[col] = 0

    # Align features
    df_aligned = df_engineered[feature_names]

    # Scale
    df_scaled = scaler.transform(df_aligned)
    
    # Predict
    predictions = model.predict(df_scaled)
    scores = -model.decision_function(df_scaled)
    
    # Add results
    df['is_anomaly'] = (predictions == -1).astype(int)
    df['anomaly_score'] = scores
    
    return df


@app.route('/')
def index():
    """Serve the dashboard HTML"""
    return send_from_directory('.', 'dashboard.html')


@app.route('/api/telemetry')
def get_telemetry():
    """
    Get latest telemetry data with anomaly predictions
    Query params:
    - limit: number of records to return (default: 150)
    """
    try:
        limit = int(request.args.get('limit', 150))
        
        # Connect to database (read-only)
        db_uri = f'file:{DB_PATH}?mode=ro'
        conn = sqlite3.connect(db_uri, uri=True)
        
        # Fetch data
        query = f"SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return jsonify([])
        
        # Predict anomalies
        df_results = predict_anomalies(df)
        
        # Convert to JSON
        result = df_results.to_dict('records')
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        db_uri = f'file:{DB_PATH}?mode=ro'
        conn = sqlite3.connect(db_uri, uri=True)
        
        # Get total records
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM telemetry")
        total_records = cursor.fetchone()[0]
        
        # Get latest 1000 for stats
        df = pd.read_sql_query(
            "SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 1000",
            conn
        )
        conn.close()
        
        if df.empty:
            return jsonify({
                'total_records': 0,
                'anomaly_rate': 0,
                'avg_altitude': 0,
                'avg_battery': 0
            })
        
        # Predict anomalies
        df_results = predict_anomalies(df)
        
        stats = {
            'total_records': total_records,
            'anomaly_rate': (df_results['is_anomaly'].sum() / len(df_results) * 100),
            'avg_altitude': df_results['altitude'].mean(),
            'avg_battery': df_results['battery_level'].mean(),
            'current_phase': df_results.iloc[0]['mode']
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': os.path.exists(DB_PATH),
        'model_loaded': model is not None
    })


@app.route('/telemetry/latest')
def get_latest_telemetry():
    """
    Get latest telemetry with history
    Query params:
    - history_limit: number of historical records (default: 150)
    """
    try:
        history_limit = int(request.args.get('history_limit', 150))
        print(f"📥 Fetching latest telemetry with history_limit={history_limit}")
        
        # Connect to database
        db_uri = f'file:{DB_PATH}?mode=ro'
        conn = sqlite3.connect(db_uri, uri=True)
        print(f"✓ Connected to database: {DB_PATH}")
        
        # Fetch data
        query = f"SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {history_limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        print(f"✓ Fetched {len(df)} records from database")
        
        if df.empty:
            print("⚠️ No data found in database")
            return jsonify({
                'latest': {},
                'history': []
            })
        
        # Predict anomalies
        print("🔮 Running anomaly detection...")
        df_results = predict_anomalies(df)
        print(f"✓ Anomaly detection complete")
        
        # Get latest and history
        latest = df_results.iloc[0].to_dict()
        history = df_results.to_dict('records')
        
        print(f"✅ Returning {len(history)} records")
        return jsonify({
            'latest': latest,
            'history': history
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        print(f"❌ ERROR in /telemetry/latest:")
        print(f"   Error: {error_msg}")
        print(f"   Stack trace:\n{stack_trace}")
        return jsonify({'error': error_msg, 'trace': stack_trace}), 500


@app.route('/status')
def get_database_status():
    """Get database connection status"""
    try:
        db_uri = f'file:{DB_PATH}?mode=ro'
        conn = sqlite3.connect(db_uri, uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM telemetry")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'connected',
            'connected': True,
            'total_records': count,
            'message': f'Database connected with {count} records'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'disconnected',
            'connected': False,
            'message': str(e)
        }), 500


@app.route('/telemetry/anomalies')
def get_anomalies():
    """Get only anomalous telemetry data"""
    try:
        limit = int(request.args.get('limit', 100))
        
        # Connect to database
        db_uri = f'file:{DB_PATH}?mode=ro'
        conn = sqlite3.connect(db_uri, uri=True)
        
        # Fetch data
        query = f"SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {limit * 2}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return jsonify([])
        
        # Predict anomalies
        df_results = predict_anomalies(df)
        
        # Filter only anomalies
        anomalies = df_results[df_results['is_anomaly'] == 1]
        
        return jsonify(anomalies.to_dict('records'))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting PUMA Dashboard API Server...")
    print(f"📊 Dashboard: http://localhost:5000")
    print(f"🔌 API Endpoints:")
    print(f"   - GET /telemetry/latest?history_limit=150")
    print(f"   - GET /status")
    print(f"   - GET /telemetry/anomalies")
    print(f"   - GET /api/telemetry")
    print(f"   - GET /api/stats")
    print(f"   - GET /api/health")
    app.run(debug=True, port=5000, host='0.0.0.0')
