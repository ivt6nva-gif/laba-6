from app.db.db import get_db

def location_all():
    """
    Повертає список всіх локацій.
    """
    db = get_db()
    cur = db.execute("SELECT id, code, name, description FROM locations")
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def location_by_code(code):
    db = get_db()
    cur = db.execute("SELECT id, code, name, description FROM locations WHERE code = ?", (code,))
    row = cur.fetchone()
    return dict(row) if row is not None else None