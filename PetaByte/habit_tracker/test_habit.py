import sqlite3

import pytest
import os
from datetime import date, timedelta
from habit_tracker.habit import HabitStreakTracker

TEST_DB_PATH = "identifier.sqlite"

@pytest.fixture(autouse=True)
def clean_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_initial_streak():
    tracker = HabitStreakTracker("user123", "exercise")
    assert tracker.get_streak() in [0, 1]

def test_increment_streak():
    tracker = HabitStreakTracker("user123", "reading", last_check_in=date.today() - timedelta(days=1), streak=1)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 2
    assert tracker.last_check_in == date.today()
    assert tracker.get_points() == 10

def test_reset_streak_after_missed_day():
    tracker = HabitStreakTracker("user123", "meditation", last_check_in=date.today() - timedelta(days=3), streak=5, points=50)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 1
    assert tracker.get_points() == 0

def test_no_change_same_day():
    today = date.today()
    tracker = HabitStreakTracker("user123", "journaling", last_check_in=today, streak=3)
    tracker.update_streak(today)
    assert tracker.get_streak() == 3
    assert tracker.last_check_in == today

def test_get_missed_days():
    tracker = HabitStreakTracker("user123", "running", last_check_in=date.today() - timedelta(days=4))
    assert tracker.get_missed_days() == 3

def test_save_and_load_streak():
    user_id = "jose123"
    habit_name = "exercise"
    tracker = HabitStreakTracker(user_id, habit_name)
    tracker.update_streak()
    tracker.save_to_db(db_path=TEST_DB_PATH)
    loaded = HabitStreakTracker.load_from_db(user_id, habit_name, db_path=TEST_DB_PATH)

    assert loaded.get_streak() == tracker.get_streak()
    assert loaded.get_points() == tracker.get_points()
    assert loaded.last_check_in == tracker.last_check_in
    assert loaded.user_id == tracker.user_id
    assert loaded.habit_name == tracker.habit_name

def test_log_completion_date():
    tracker = HabitStreakTracker("user123", "yoga")
    tracker.log_completion_date(today=date.today(), db_path=TEST_DB_PATH)

    import sqlite3
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habit_history WHERE user_id = ? AND habit_name = ?", ("user123", "yoga"))
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == "user123"
    assert result[1] == "yoga"
    assert result[2] == date.today().isoformat()

def test_delete_habit():
    tracker = HabitStreakTracker("user123", "delete_me")
    tracker.update_streak()
    tracker.save_to_db(db_path=TEST_DB_PATH)
    tracker.log_completion_date(db_path=TEST_DB_PATH)

    HabitStreakTracker.delete_habit("user123", "delete_me", db_path=TEST_DB_PATH)

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habit_streaks WHERE user_id = ? AND habit_name = ?", ("jose123", "delete_me"))
    assert cursor.fetchone() is None

    cursor.execute("SELECT * FROM habit_history WHERE user_id = ? AND habit_name = ?", ("jose123", "delete_me"))
    assert cursor.fetchone() is None

    conn.close()
