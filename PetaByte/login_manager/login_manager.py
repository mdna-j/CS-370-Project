import sqlite3
import hashlib
import os

DB_PATH = os.path.join("petabyte", "database", "petabyte.db")

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
            try:
                cursor=conn.cursor()
                cursor.execute("INSERT INTO Users (Username) VALUES (?)", (username,))
                user_id=cursor.lastrowid
                cursor.execute("INSERT INTO Passwords (User_ID,password_hash) VALUES (?,?)", (user_id,password_hashed))
                conn.commit()
            except sqlite3.IntegrityError:##unessecary except modify to catch password errors? or is validation at earlier stage enough?
                raise Exception("Username already exists.")


    @staticmethod
    def authenticate_user(username, password):
        hashed = LoginManager.hash_password(password)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM Users,Passwords WHERE username = ? AND password_hash = ?", (username, hashed))
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
            account_id = conn.execute("SELECT Account_ID FROM * WHERE username = ?",(username))
            cur = conn.execute("DELETE * FROM Users WHERE ", (account_id,))
            return Exception("account deleted")

        ## verify account is deleted and cascades through database
