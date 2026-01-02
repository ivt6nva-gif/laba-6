import sqlite3
from pathlib import Path
import os

# Шлях до папки backend/app/db
DB_DIR = Path(__file__).resolve().parent / "backend" / "app" / "db"
DB_FILE = DB_DIR / "users.db"

# Створюємо папку backend/app/db, якщо її немає
DB_DIR.mkdir(parents=True, exist_ok=True)

# Видаляємо старий файл, щоб точно мати свіжу базу
if DB_FILE.exists():
    DB_FILE.unlink()
    print(f"Старий файл видалено: {DB_FILE}")

print(f"Створюємо базу даних у: {DB_FILE}")

# Підключаємося — файл створиться саме в backend/app/db/
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Створюємо таблицю locations з колонкою code (бо твій код шукає за code)
cur.execute("""
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT
)
""")

# Додаємо тестові локації
cur.executemany("INSERT INTO locations (code, name, description) VALUES (?, ?, ?)", [
    ("office", "Офіс", "Головний офіс компанії"),
    ("warehouse", "Склад", "Склад готової продукції"),
    ("lab", "Лабораторія", "Тестова лабораторія")
])

# Створюємо інші таблиці (щоб не було помилок пізніше)
cur.execute("""
CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    serial TEXT,
    type TEXT,
    fw_version TEXT,
    location_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    ts TEXT,
    temperature_c REAL,
    humidity_pct REAL,
    voltage_v REAL,
    co_ppm REAL,
    no2_ppb REAL,
    light_lux REAL
)
""")

# Додаємо тестові сенсори, прив'язані до локацій (location_id 1..3)
cur.executemany(
    "INSERT INTO sensors (code, serial, type, fw_version, location_id) VALUES (?, ?, ?, ?, ?)",
    [
        ("S-001", "SN1001", "env", "1.0.0", 1),
        ("S-002", "SN1002", "env", "1.0.0", 1),
        ("S-101", "SN1101", "env", "1.0.0", 2),
        ("S-201", "SN1201", "env", "1.0.0", 3),
    ],
)

# Додаємо кілька тестових вимірювань для першого сенсора
from datetime import datetime, timedelta

# Функція для генерації синтетичних вимірювань
def generate_readings(sensor_id: int, start: datetime, points: int, delta_minutes: int):
    rows = []
    for i in range(points):
        ts = (start + timedelta(minutes=i * delta_minutes)).strftime("%Y-%m-%d %H:%M:%S")
        # прості синусоїдальні/шумові генератори для кожної метрики
        temp = 20 + 5 * __import__('math').sin(i / 3.0) + (i % 3) * 0.2
        hum = 40 + 20 * abs(__import__('math').sin(i / 5.0)) + (i % 4) * 0.3
        volt = 3.7 + ((i % 10) - 5) * 0.01
        co = max(0.0, 0.1 + 0.05 * __import__('math').sin(i / 4.0))
        no2 = max(0.0, 5 + 3 * __import__('math').sin(i / 6.0))
        light = max(0.0, 100 + 50 * __import__('math').sin(i / 2.0))
        rows.append((sensor_id, ts, round(temp, 2), round(hum, 2), round(volt, 2), round(co, 3), round(no2, 2), round(light, 1)))
    return rows

# Згенеруємо по 48 точок (прибл. 2 дні з кроком 1 година) для кожного сенсора
base = datetime(2025, 12, 14, 12, 0, 0)
all_rows = []
all_rows += generate_readings(1, base, points=48, delta_minutes=60)
all_rows += generate_readings(2, base, points=48, delta_minutes=60)
all_rows += generate_readings(3, base, points=48, delta_minutes=60)
all_rows += generate_readings(4, base, points=48, delta_minutes=60)

cur.executemany(
    "INSERT INTO readings (sensor_id, ts, temperature_c, humidity_pct, voltage_v, co_ppm, no2_ppb, light_lux) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    all_rows,
)

conn.commit()
conn.close()

print("База даних users.db успішно створена в backend/app/db/")
print("Тепер запускай Flask — все працюватиме!")