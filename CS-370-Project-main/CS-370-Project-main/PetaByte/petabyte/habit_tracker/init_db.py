import sqlite3


def initialize_habit_db():
    conn = sqlite3.connect("identifier.sqlite")
    cursor = conn.cursor()

    # Habit streaks table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS habit_streaks
                   (
                       user_id TEXT,
                       habit_name TEXT,
                       last_check_in TEXT,
                       streak INTEGER,
                       PRIMARY KEY (user_id, habit_name)
                   )
                   """)

    conn.commit()
    conn.close()
    print("Habit streak table initialized successfully.")


if __name__ == "__main__":
    initialize_habit_db()
