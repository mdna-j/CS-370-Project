from datetime import date, timedelta, datetime
import sqlite3
from plyer import notification  # For desktop notifications

class HabitStreakTracker:
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

    def save_to_db(self, db_path="identifier.sqlite"):
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS habit_streaks
                       (
                           user_id       INTEGER,
                           habit_name    TEXT,
                           last_check_in TEXT,
                           streak        INTEGER,
                           points        INTEGER,
                           PRIMARY KEY (user_id, habit_name),
                           FOREIGN KEY (user_id) REFERENCES users (id)
                       )
                       ''')

        cursor.execute('''
            INSERT OR REPLACE INTO habit_streaks 
            (user_id, habit_name, last_check_in, streak, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, self.habit_name, self.last_check_in.isoformat(), self.streak, self.points))

        conn.commit()
        conn.close()

    def log_completion_date(self, today=None, db_path="identifier.sqlite"):
        today = today or date.today()
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_history (
            user_id INTEGER,
            habit_name TEXT,
            date_completed TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            INSERT INTO habit_history (user_id, habit_name, date_completed)
            VALUES (?, ?, ?)
        ''', (self.user_id, self.habit_name, today.isoformat()))

        conn.commit()
        conn.close()

    @classmethod
    def load_from_db(cls, user_id, habit_name, db_path="identifier.sqlite"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_check_in, streak, points FROM habit_streaks
            WHERE user_id = ? AND habit_name = ?
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
    def delete_habit(user_id, habit_name, db_path="identifier.sqlite"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habit_streaks WHERE user_id = ? AND habit_name = ?', (user_id, habit_name))
        cursor.execute('DELETE FROM habit_history WHERE user_id = ? AND habit_name = ?', (user_id, habit_name))
        conn.commit()
        conn.close()

    def apply_to_pet(self, pet):
        if self.streak >= 5:
            pet.update_happiness(10)  # You define this method in your Pet class
        elif self.get_missed_days() >= 2:
            pet.update_happiness(-5)

    def notify_user_missed(self, missed_days):
        notification.notify(
            title="Missed Habit Alert",
            message=f"You've missed {missed_days} day(s) of '{self.habit_name}'!",
            timeout=5
        )
