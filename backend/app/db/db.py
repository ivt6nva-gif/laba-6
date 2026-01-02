import os
import sqlite3
from flask import g

# Шлях до файлу бази даних відносно цього модуля
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, "users.db")

def get_db():
    """
    Повертає з'єднання з базою даних.
    Зберігає з'єднання в g для використання протягом одного запиту.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # дозволяє використовувати dict(row)
    return db


def close_db(exception=None):
    """
    Закриває з'єднання з базою даних, якщо воно існує.
    Викликається автоматично Flask після завершення запиту.
    """
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()