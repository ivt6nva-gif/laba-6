from typing import Optional, Dict, Any
import sqlite3
from app.db.users_db import users_by_user_name, create_user
from app.security.password_hash import hash_password

def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    return users_by_user_name(username)

def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    row = users_by_user_name(username)
    if row is None:
        return None
    stored_salt = row["salt"]
    stored_hash = row["password"]
    _, check_hash = hash_password(password, stored_salt)
    if check_hash != stored_hash:
        return None
    return {"id": row["id"], "username": row["username"]}

def generate_user (username: str, password: str) -> int:
    new_user = create_user(username, password)
    return new_user