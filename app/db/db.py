import sqlite3
from flask import g
from app.config import Config

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(
        Config.DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES,)

    g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db() -> None:
    db = get_db()
    db.executescript(
"""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
salt TEXT NOT NULL
);
"""
)
    db.commit()
    db.close()