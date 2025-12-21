import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "SUPER_SECRET")
    DATABASE = os.environ.get("DATABASE_URL",
    str(BASE_DIR / "app" / "db" / "users.db"),
)