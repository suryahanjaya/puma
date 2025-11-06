import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.scaler = StandardScaler()

    def fit_predict(self, df):
        features = ["altitude", "speed", "battery_level"]
        X = df[features]
        X_scaled = self.scaler.fit_transform(X)

        df["anomaly"] = self.model.fit_predict(X_scaled)  # -1 = anomaly, 1 = normal
        return df

if __name__ == "__main__":
    df = pd.read_csv("data/telemetry_dummy.csv")
    detector = AnomalyDetector()
    df_result = detector.fit_predict(df)
    df_result.to_csv("data/telemetry_with_anomaly.csv", index=False)
    print("Anomaly detection complete. Saved to data/telemetry_with_anomaly.csv")
