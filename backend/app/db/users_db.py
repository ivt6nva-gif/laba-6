from app.db.db import get_db, close_db
from app.security.password_hash import hash_password

def users_by_user_name(username):
    database = get_db()
    cur = database.execute("SELECT id, username, password, salt FROM users WHERE username = ?",(username,),)
    res = cur.fetchone()
    return res

def create_user(username: str, password: str) -> int:
    database = get_db()
    salt, pwd_hash = hash_password(password)
    cur = database.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",(username, pwd_hash, salt),)
    
    database.commit()
    user_id = cur.lastrowid
    return {
    "id": user_id,
    "username": username,}