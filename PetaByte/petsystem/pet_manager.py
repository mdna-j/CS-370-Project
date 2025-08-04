import sqlite3
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
    def set_image(image):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetMedia (pet_image_1) VALUES (?)", (image,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting image into Database")

    @staticmethod
    def set_audio(audio):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetMedia(pet_sound_1) VALUES (?)", (audio,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting audio into Database")

    @staticmethod
    def get_audio(pet_media_ptr):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_sound_1 FROM PetMedia WHERE pet_media_ptr = ?  ", (pet_media_ptr,))
            return cur.fetchone() is not None

    @staticmethod
    def get_image(pet_media_ptr):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_image_1 FROM PetMedia WHERE pet_media_ptr = ?  ", (pet_media_ptr,))
            return cur.fetchone() is not None

    @staticmethod
    def set_pet_mood(moodvalue):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetState(pet_mood) VALUES (?)", (moodvalue,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting audio into Database")


    @staticmethod
    def get_pet_mood(mood):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_image_1 FROM PetMedia WHERE pet_media_ptr = ?  ", (mood,))
            return cur.fetchone() is not None

    @staticmethod
    def set_pet_need(needvalue):
        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute("INSERT INTO PetState(pet_need_1) VALUES (?)", (needvalue,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise Exception("error inserting audio into Database")

    @staticmethod
    def get_pet_need(need):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT pet_need_1 FROM PetState WHERE pet_need_1 = ? ", (need,))
            return cur.fetchone() is not None
