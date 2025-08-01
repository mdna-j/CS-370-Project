from datetime import date, timedelta, datetime
import sqlite3
from plyer import notification  # For desktop notifications

class Habit_Manager:

    db_path = "PetaByte/database/petabyte.db"

    def __init__(self, user_id, habit_name, last_check_in=None, streak=1, points=0):
        self.user_id = user_id
        self.habit_name = habit_name
        self.last_check_in = last_check_in or (date.today() - timedelta(days=1))
        self.streak = streak
        self.points = points

    def update_streak(self, today=None):
        today = today or date.today()
        missed_days = (today - self.last_check_in).days - 1

        if today == self.last_check_in + timedelta(days=1):
            self.streak += 1
            self.points += 10
        elif today > self.last_check_in + timedelta(days=1):
            self.streak = 1
            self.points = 0
            self.notify_user_missed(missed_days)

        self.last_check_in = today
        self.log_completion_date(today)

    def get_streak(self):
        return self.streak

    def get_points(self):
        return self.points

    def get_missed_days(self, today=None):
        today = today or date.today()
        delta = (today - self.last_check_in).days
        return max(0, delta - 1)

    def __repr__(self):
        return (f"<HabitStreakTracker(user_id={self.user_id}, habit={self.habit_name}, "
                f"streak={self.streak}, points={self.points}, last_check_in={self.last_check_in})>")

    def save_to_db(self):
        conn = sqlite3.connect(Habit_Manager.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        with open("petabyte/habit_tracker/Habits.sql", "r") as ACC:
            conn.executescript(ACC.read())
        conn.commit()
        conn.close()

    def update_db(self):
        conn = sqlite3.connect(Habit_Manager.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO Habits 
            (user_id, habit_name, last_check_in, streak, points) VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, self.habit_name, self.last_check_in.isoformat(), self.streak, self.points))

        conn.commit()
        conn.close()

    def log_completion_date(self, today=None):
        today = today or date.today()
        conn = sqlite3.connect(Habit_Manager.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        with open("petabyte/Habit_tracker/Habits_Log.sql", "r") as ACC:
            conn.executescript(ACC.read())

        cursor.execute('''
            INSERT INTO Habits_Log (Habit_id, habit_name, timeptr)
            VALUES (?, ?, ?)
        ''', (self.user_id, self.habit_name, today.isoformat()))

        conn.commit()
        conn.close()

    @classmethod
    def load_from_db(cls, user_id, habit_name):
        conn = sqlite3.connect(Habit_Manager.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_check_in, streak, points FROM Habits_Log
            WHERE Habit_ID = ? AND habit_name = ?
        ''', (user_id, habit_name))

        result = cursor.fetchone()
        conn.close()

        if result:
            last_check_in = datetime.strptime(result[0], "%Y-%m-%d").date()
            streak = result[1]
            points = result[2]
            return cls(user_id, habit_name, last_check_in, streak, points)
        else:
            return cls(user_id, habit_name)

    @staticmethod
    def delete_habit(user_id, habit_name):
        conn = sqlite3.connect(Habit_Manager.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Habits_Log WHERE Habits_Log.Habit_ID= ? AND habit_name = ?', (user_id, habit_name))
        cursor.execute('DELETE FROM habit_history WHERE user_id = ? AND habit_name = ?', (user_id, habit_name))
        conn.commit()
        conn.close()

    def apply_to_pet(self, pet):
        if self.streak >= 5:
            pet.update_happiness(10)  # You define this method in your Pet class
        elif self.get_missed_days() >= 2:
            pet.update_happiness(-5)# should be handled by petsystem

    def notify_user_missed(self, missed_days):
        notification.notify(
            title="Missed Habit Alert",
            message=f"You've missed {missed_days} day(s) of '{self.habit_name}'!",
            timeout=5
        )
