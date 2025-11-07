import sqlite3, time, os
from datetime import datetime
DB="data/deliveries.db"
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS deliveries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  client TEXT,
  lat REAL,
  lon REAL,
  meteo TEXT,
  temperature REAL,
  traffic TEXT
)
""")
conn.commit()

class RealTimeTracker:
    def __init__(self):
        self.conn = conn
        self.cursor = cursor

    def record_point(self, client, lat, lon, meteo, temp, traffic):
        self.cursor.execute("INSERT INTO deliveries (timestamp, client, lat, lon, meteo, temperature, traffic) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (datetime.utcnow().isoformat(), client, lat, lon, meteo, temp, traffic))
        self.conn.commit()
