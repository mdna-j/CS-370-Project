import sqlite3


def initialize_habit_db():
    conn = sqlite3.connect("identifier.sqlite")
    cursor = conn.cursor()

    # Habit streaks table
    cursor.execute("""
                       CREATE TABLE IF NOT EXISTS habit_history (
        user_id TEXT,
        habit_name TEXT,
        date_completed TEXT
    )

                   """)

    conn.commit()
    conn.close()
    print("Habit history initialized successfully.")


if __name__ == "__main__":
    initialize_habit_db()
