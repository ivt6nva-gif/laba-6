import sqlite3
from pathlib import Path

script_dir = Path(__file__).resolve().parent
db_path = script_dir / ".." / "backend" / "app" / "db" / "users.db"

print(f"Checking DB at: {db_path.resolve()}")
if not db_path.exists():
    print("DB file not found")
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path.resolve()))
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("\nLocations:")
for r in cur.execute("SELECT id, code, name FROM locations ORDER BY id").fetchall():
    print(dict(r))

print("\nSensors:")
sensors = cur.execute("SELECT id, code, serial, location_id FROM sensors ORDER BY id").fetchall()
for r in sensors:
    print(dict(r))

print("\nSensors count by location:")
for r in cur.execute("SELECT location_id, COUNT(*) as cnt FROM sensors GROUP BY location_id").fetchall():
    print(dict(r))

print("\nReadings count by sensor:")
for r in cur.execute("SELECT sensor_id, COUNT(*) as cnt FROM readings GROUP BY sensor_id").fetchall():
    print(dict(r))

conn.close()
