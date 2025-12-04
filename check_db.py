import sqlite3

conn = sqlite3.connect('data/uav_telemetry.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", tables)

# If there are tables, show their schema
for table in tables:
    table_name = table[0]
    print(f"\nSchema for table '{table_name}':")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Show count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  Total records: {count}")

conn.close()
