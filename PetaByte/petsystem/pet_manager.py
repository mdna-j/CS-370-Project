import sqlite3
import hashlib
import os

DB_PATH = os.path.join("petabyte", "database", "petabyte.db")

class PetManager:
    @staticmethod
    def initialize():
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            with open("petabyte/login_manager/PetState.sql", "r") as ACC:
                conn.executescript(ACC.read())
            with open("petabyte/login_manager/PetMedia.sql", "r") as f:
                conn.executescript(f.read())

    @staticmethod
    def Add_Image(image):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetMedia (pet_image_1) VALUES (?)", (image,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting image into Database")

    @staticmethod
    def Add_Audio(audio):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetMedia(pet_sound_1) VALUES (?)", (audio,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting audio into Database")

    @staticmethod
    def Fetch_Audio(pet_media_ptr):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_sound_1 FROM PetMedia WHERE pet_media_ptr = ?  ", (pet_media_ptr,))
            return cur.fetchone() is not None

    @staticmethod
    def Fetch_Image(pet_media_ptr):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_image_1 FROM PetMedia WHERE pet_media_ptr = ?  ", (pet_media_ptr,))
            return cur.fetchone() is not None

