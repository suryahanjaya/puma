import pandas as pd
from sklearn.ensemble import IsolationForest

# Load data dummy
df = pd.read_csv("data/telemetry_dummy.csv")

# Buat model deteksi anomali
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df[["altitude", "speed", "battery_level"]])

# Prediksi anomali
df["anomaly"] = model.predict(df[["altitude", "speed", "battery_level"]])

# Simpan hasil
df.to_csv("data/telemetry_with_anomaly.csv", index=False)
print("Anomaly detection complete: data/telemetry_with_anomaly.csv")
