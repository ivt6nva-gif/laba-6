import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

DB_PATH = Path("backend/app/db/users.db")

# Видаляємо старий файл, якщо є
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Створюємо таблицю локацій
cur.execute("""
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
""")

# Створюємо таблицю сенсорів
cur.execute("""
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    serial TEXT,
    type TEXT,
    fw_version TEXT,
    location_id INTEGER,
    FOREIGN KEY (location_id) REFERENCES locations (id)
)
""")

# Створюємо таблицю вимірювань
cur.execute("""
CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    ts TEXT NOT NULL,
    temperature_c REAL,
    humidity_pct REAL,
    voltage_v REAL,
    co_ppm REAL,
    no2_ppb REAL,
    light_lux REAL,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id)
)
""")

# Додаємо тестові локації
locations = [
    ("Офіс", "Головний офіс компанії"),
    ("Склад", "Склад готової продукції"),
    ("Лабораторія", "Тестова лабораторія")
]
cur.executemany("INSERT INTO locations (name, description) VALUES (?, ?)", locations)

# Додаємо сенсори
sensors = [
    ("SENS-01", "A001", "air_quality", "1.2.3", 1),
    ("SENS-02", "A002", "air_quality", "1.2.3", 1),
    ("SENS-03", "B001", "weather", "2.0.1", 2),
    ("SENS-04", "B002", "weather", "2.0.1", 2),
    ("SENS-05", "C001", "env_monitor", "1.5.0", 3),
    ("SENS-06", "C002", "env_monitor", "1.5.0", 3),
]
cur.executemany("INSERT INTO sensors (code, serial, type, fw_version, location_id) VALUES (?, ?, ?, ?, ?)", sensors)

# Генеруємо тестові вимірювання (по 200 записів на кожен сенсор за грудень 2025)
start_date = datetime(2025, 12, 1, 0, 0, 0)
for sensor_id in range(1, 7):
    current_time = start_date
    for _ in range(200):
        ts = current_time.strftime("%Y-%m-%d %H:%M:%S")
        temperature = round(random.uniform(18, 28), 2)
        humidity = round(random.uniform(30, 70), 2)
        voltage = round(random.uniform(3.2, 3.6), 2)
        co = round(random.uniform(0.1, 2.0), 2)
        no2 = round(random.uniform(5, 50), 1)
        light = round(random.uniform(100, 1000), 0)

        cur.execute("""
            INSERT INTO readings (sensor_id, ts, temperature_c, humidity_pct, voltage_v, co_ppm, no2_ppb, light_lux)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sensor_id, ts, temperature, humidity, voltage, co, no2, light))

        current_time += timedelta(minutes=30)  # кожні 30 хвилин

conn.commit()
conn.close()

print("Тестова база users.db успішно створена з даними!")
print("Розташування: backend/app/db/users.db")