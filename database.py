import sqlite3
import os
from pathlib import Path

# Определяем, где мы находимся: на Bothost (есть папка /app) или на ПК
if os.path.exists("/app"):
    DATA_DIR = Path("/app/data")
else:
    DATA_DIR = Path(".")

# Создаем папку, если ее нет
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_NAME = DATA_DIR / "game.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 50,
            engine_fixed INTEGER DEFAULT 0,
            body_fixed INTEGER DEFAULT 0,
            wheels_fixed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return get_user(user_id)
        
    return {
        "user_id": user[0], "coins": user[1], 
        "engine": user[2], "body": user[3], "wheels": user[4]
    }

def update_user(user_id, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for key, value in kwargs.items():
        cursor.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def reset_car(user_id):
    update_user(user_id, engine_fixed=0, body_fixed=0, wheels_fixed=0)