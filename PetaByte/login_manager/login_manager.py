import sqlite3
import hashlib
import os

DB_PATH = os.path.join("petabyte", "database", "petabyte.db")

class LoginManager:
    @staticmethod
    def initialize():
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            with open("petabyte/login_manager/schema.sql", "r") as f:
                conn.executescript(f.read())

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username, password):
        hashed = LoginManager.hash_password(password)
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("Username already exists.")

    @staticmethod
    def authenticate_user(username, password):
        hashed = LoginManager.hash_password(password)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, hashed))
            return cur.fetchone() is not None
