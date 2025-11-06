import pandas as pd
import random

def generate_dummy_data(n=1000):
    data = []
    for i in range(n):
        data.append({
            "timestamp": i,
            "altitude": random.uniform(100, 5000),
            "speed": random.uniform(60, 300),
            "battery_level": random.uniform(20, 100),
            "gps_lat": -7.27 + random.uniform(-0.01, 0.01),
            "gps_lon": 112.74 + random.uniform(-0.01, 0.01)
        })
    df = pd.DataFrame(data)
    df.to_csv("data/telemetry_dummy.csv", index=False)
    print("Dummy telemetry data created: data/telemetry_dummy.csv")

if __name__ == "__main__":
    generate_dummy_data()
