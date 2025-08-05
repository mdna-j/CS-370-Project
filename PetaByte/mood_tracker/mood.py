import sqlite3
import datetime
import os

DB_PATH = os.path.join("PetaByte", "database", "petabyte.db")

# Create a table for mood history if it doesn't exist
def init_mood_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Mood_History (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TEXT,
                mood TEXT,
                source TEXT CHECK(source IN ('user', 'idle')) DEFAULT 'user',
                FOREIGN KEY(user_id) REFERENCES Users(Account_ID)
            )
        ''')
        conn.commit()


# Record a mood
def log_mood(user_id, mood, source="user"):
    timestamp = datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Mood_History (user_id, timestamp, mood, source)
            VALUES (?, ?, ?, ?)
        ''', (user_id, timestamp, mood, source))
        conn.commit()


# Retrieve all mood entries for a user
def get_mood_history(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, mood, source FROM Mood_History
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        return cursor.fetchall()


# Analyze mood streaks (past 7 days)
def get_mood_summary(user_id):
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT mood, COUNT(*) FROM Mood_History
            WHERE user_id = ? AND timestamp >= ?
            GROUP BY mood
            ORDER BY COUNT(*) DESC
        ''', (user_id, one_week_ago.isoformat()))
        return cursor.fetchall()


# Reflect mood on pet's behavior
def get_latest_mood(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT mood FROM Mood_History
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (user_id,))
        row = cursor.fetchone()
        return row[0] if row else "neutral"
