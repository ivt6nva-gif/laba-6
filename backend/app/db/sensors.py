from app.db.db import get_db

def sensors_all():
    """
    Повертає список всіх сенсорів.
    """
    db = get_db()
    cur = db.execute("SELECT * FROM sensors")  # без лапок навколо назви таблиці
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def get_all_measurements_by_sensor(sensor_id):
    """
    Повертає всі вимірювання для заданого сенсора.
    """
    db = get_db()
    cur = db.execute(
        "SELECT * FROM readings WHERE sensor_id = ?",
        (sensor_id,)
    )
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def get_measurement_by_sensor_from_to(sensor_id, time_from, time_to):
    """
    Повертає вимірювання сенсора за діапазоном дат.
    """
    db = get_db()
    cur = db.execute(
        """SELECT * FROM readings
           WHERE sensor_id = ?
             AND ts BETWEEN ? AND ?
           ORDER BY ts ASC""",
        (sensor_id, time_from, time_to)
    )
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def sensors_by_location(location_id):
    """
    Повертає сенсори для вказаної локації, відсортовані за кодом.
    """
    db = get_db()
    cur = db.execute(
        "SELECT * FROM sensors WHERE location_id = ? ORDER BY code ASC",
        (location_id,)
    )
    rows = cur.fetchall()
    return [dict(row) for row in rows]