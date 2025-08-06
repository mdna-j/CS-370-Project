import sqlite3
import hashlib
import os
import re

DB_PATH = os.path.join("PetaByte", "database", "petabyte.db")


class LoginManager:

    @staticmethod
    def initialize():
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            with open("petabyte/login_manager/Users.sql", "r") as ACC:
                conn.executescript(ACC.read())
            with open("petabyte/login_manager/Passwords.sql", "r") as f:
                conn.executescript(f.read())

    @staticmethod
    def hash_password(password):

        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username, password):
        password_hashed = LoginManager.hash_password(password)

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Users (username) VALUES (?)", (username,))
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO Passwords (user_id,password_hash) VALUES (?,?)", (user_id, password_hashed))
                conn.commit()
            except sqlite3.IntegrityError:  ##unessecary except modify to catch password errors? or is validation at earlier stage enough?
                raise Exception("Failed to register user.")

    @staticmethod
    def authenticate_user(username, password):
        hashed = LoginManager.hash_password(password)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM Users,Passwords WHERE Users.username = ? AND Passwords.password_hash = ?",
                               (username, hashed))
            return cur.fetchone() is not None

    @staticmethod
    def get_user_id(username):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Account_ID FROM Users WHERE Username = ?", (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def delete_account(username):
        with sqlite3.connect(DB_PATH) as conn:
            account_id = conn.execute("SELECT Account_ID FROM * WHERE username = ?", (username))
            conn.execute("DELETE * FROM Users WHERE ", (account_id,))
            return Exception("account deleted")

    @staticmethod
    def validate(username, password):
        from login_manager.login_screen import LoginScreen
        if username.text.strip() != "":
            if re.search(r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!@#$%&*-]).{8,20}$", password.text.strip()):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def reset_password(username, new_password):
        hashed = LoginManager.hash_password(new_password)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Account_ID FROM Users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                cursor.execute("UPDATE Passwords SET password_hash = ? WHERE User_ID = ?", (hashed, user[0]))
                conn.commit()
                return True
            else:
                return False
