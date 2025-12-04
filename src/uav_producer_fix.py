import sqlite3
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- Konfigurasi Path ---
# Get parent directory (uav-mlops-dashboard) instead of src/data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # src folder
PARENT_DIR = os.path.dirname(SCRIPT_DIR)  # uav-mlops-dashboard folder
DATA_DIR = os.path.join(PARENT_DIR, "data")  # uav-mlops-dashboard/data
DB_PATH = os.path.join(DATA_DIR, "uav_telemetry.db")
CSV_PATH = os.path.join(DATA_DIR, "telemetry_data.csv")
print(f"🔍 DEBUG: CSV_PATH = {CSV_PATH}")
print(f"🔍 DEBUG: CSV exists? {os.path.exists(CSV_PATH)}")
# ------------------------
