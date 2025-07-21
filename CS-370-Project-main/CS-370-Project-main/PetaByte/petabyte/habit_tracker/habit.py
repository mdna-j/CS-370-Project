from datetime import date, timedelta, datetime
import sqlite3

class HabitStreakTracker:
    def __init__(self, user_id, habit_name, last_check_in=None, streak=1):
        self.user_id = user_id
        self.habit_name = habit_name
        self.last_check_in = last_check_in or (date.today() - timedelta(days=1))
        self.streak = streak

    def update_streak(self, today=None):
        today = today or date.today()
        if today == self.last_check_in + timedelta(days=1):
            self.streak += 1
        elif today > self.last_check_in + timedelta(days=1):
            self.streak = 1  # Reset if user skipped a day

        self.last_check_in = today

    def get_streak(self):
        return self.streak

    def __repr__(self):
        return f"<HabitStreakTracker(user_id={self.user_id}, habit={self.habit_name}, streak={self.streak}, last_check_in={self.last_check_in})>"

    def save_to_db(self, db_path="identifier.sqlite"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_streaks (
                user_id TEXT,
                habit_name TEXT,
                last_check_in TEXT,
                streak INTEGER,
                PRIMARY KEY (user_id, habit_name)
            )
        ''')

        cursor.execute('''
            INSERT OR REPLACE INTO habit_streaks (user_id, habit_name, last_check_in, streak)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, self.habit_name, self.last_check_in.isoformat(), self.streak))

        conn.commit()
        conn.close()

    @classmethod
    def load_from_db(cls, user_id, habit_name, db_path="identifier.sqlite"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_check_in, streak FROM habit_streaks
            WHERE user_id = ? AND habit_name = ?
        ''', (user_id, habit_name))

        result = cursor.fetchone()
        conn.close()

        if result:
            last_check_in = datetime.strptime(result[0], "%Y-%m-%d").date()
            streak = result[1]
            return cls(user_id, habit_name, last_check_in, streak)
        else:
            return cls(user_id, habit_name)  # default start
