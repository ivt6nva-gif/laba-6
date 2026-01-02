import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import math

DB_PATH = Path(__file__).resolve().parent / '..' / 'backend' / 'app' / 'db' / 'users.db'
DB_PATH = DB_PATH.resolve()
print('DB:', DB_PATH)
if not DB_PATH.exists():
    raise SystemExit('DB not found')

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

# simple generator
def generate_readings(sensor_id: int, start: datetime, points: int, delta_minutes: int):
    rows = []
    for i in range(points):
        ts = (start + timedelta(minutes=i * delta_minutes)).strftime('%Y-%m-%d %H:%M:%S')
        temp = 15 + 10 * math.sin(i / 6.0) + (sensor_id - 1) * 0.5
        hum = 30 + 25 * abs(math.sin(i / 5.0))
        volt = 3.7 + ((i % 10) - 5) * 0.01
        co = max(0.0, 0.1 + 0.05 * math.sin(i / 4.0))
        no2 = max(0.0, 5 + 3 * math.sin(i / 6.0))
        light = max(0.0, 50 + 100 * max(0, math.sin(i / 2.0)))
        rows.append((sensor_id, ts, round(temp,2), round(hum,2), round(volt,2), round(co,3), round(no2,2), round(light,1)))
    return rows

# choose a base that doesn't collide with existing timestamps
base = datetime(2025, 12, 10, 6, 0, 0)
all_rows = []
for sensor in [1,2,3,4]:
    all_rows += generate_readings(sensor, base, points=96, delta_minutes=30)

print('Inserting', len(all_rows), 'rows')
cur.executemany(
    'INSERT INTO readings (sensor_id, ts, temperature_c, humidity_pct, voltage_v, co_ppm, no2_ppb, light_lux) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
    all_rows
)
conn.commit()
print('Done')
conn.close()
