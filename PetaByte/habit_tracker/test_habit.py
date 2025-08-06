import os
import sqlite3
import pytest
from datetime import date, timedelta
from habit_tracker.habit import Habit_Manager

TEST_DB_PATH = "petabyte_test.db"

@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            pass
    yield
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            pass

def test_initial_streak():
    tracker = Habit_Manager("user1", "exercise", db_path=TEST_DB_PATH)
    assert tracker.get_streak() == 1

def test_increment_streak():
    tracker = Habit_Manager("user1", "reading", last_check_in=date.today() - timedelta(days=1), streak=1, db_path=TEST_DB_PATH)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 2
    assert tracker.get_points() == 10

def test_reset_streak():
    tracker = Habit_Manager("user1", "meditation", last_check_in=date.today() - timedelta(days=3), streak=5, points=50, db_path=TEST_DB_PATH)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 1
    assert tracker.get_points() == 0

def test_same_day_update():
    today = date.today()
    tracker = Habit_Manager("user1", "journaling", last_check_in=today, streak=3, db_path=TEST_DB_PATH)
    tracker.update_streak(today)
    assert tracker.get_streak() == 3

def test_missed_days():
    tracker = Habit_Manager("user1", "running", last_check_in=date.today() - timedelta(days=4), db_path=TEST_DB_PATH)
    assert tracker.get_missed_days() == 3

def test_save_and_load():
    user_id = "jose123"
    habit_name = "exercise"
    tracker = Habit_Manager(user_id, habit_name, db_path=TEST_DB_PATH)
    tracker.update_streak()
    tracker.save_to_db()
    loaded = Habit_Manager.load_from_db(user_id, habit_name, db_path=TEST_DB_PATH)

    assert loaded.get_streak() == tracker.get_streak()
    assert loaded.get_points() == tracker.get_points()
    assert loaded.last_check_in == tracker.last_check_in

def test_log_completion_date():
    tracker = Habit_Manager("user1", "yoga", db_path=TEST_DB_PATH)
    tracker.log_completion_date(today=date.today())

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Habits_Log WHERE Habit_ID = ? AND habit_name = ?", ("user1", "yoga"))
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == "user1"
    assert result[1] == "yoga"

def test_delete_habit():
    tracker = Habit_Manager("user1", "delete_me", db_path=TEST_DB_PATH)
    tracker.update_streak()
    tracker.save_to_db()

    Habit_Manager.delete_habit("user1", "delete_me", db_path=TEST_DB_PATH)

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Habits WHERE user_id = ? AND habit_name = ?", ("user1", "delete_me"))
    assert cursor.fetchone() is None
    cursor.execute("SELECT * FROM Habits_Log WHERE Habit_ID = ? AND habit_name = ?", ("user1", "delete_me"))
    assert cursor.fetchone() is None
    conn.close()
