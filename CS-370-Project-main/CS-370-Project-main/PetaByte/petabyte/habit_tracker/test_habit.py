import pytest
import os
from datetime import date, timedelta
from habit_tracker.habit import HabitStreakTracker


TEST_DB_PATH = "identifier.sqlite"

def test_initial_streak():
    tracker = HabitStreakTracker("jose123", "exercise")
    assert tracker.get_streak() in [0, 1]

def test_increment_streak():
    tracker = HabitStreakTracker("jose123", "reading", last_check_in=date.today() - timedelta(days=1), streak=1)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 2
    assert tracker.last_check_in == date.today()

def test_reset_streak_after_missed_day():
    tracker = HabitStreakTracker("jose123", "meditation", last_check_in=date.today() - timedelta(days=2), streak=5)
    tracker.update_streak(date.today())
    assert tracker.get_streak() == 1
    assert tracker.last_check_in == date.today()

def test_no_change_same_day():
    today = date.today()
    tracker = HabitStreakTracker("jose123", "journaling", last_check_in=today, streak=3)
    tracker.update_streak(today)
    assert tracker.get_streak() == 3
    assert tracker.last_check_in == today

@pytest.fixture(autouse=True)
def clean_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_save_and_load_streak():
    user_id = "jose123"
    habit_name = "exercise"

    tracker = HabitStreakTracker(user_id, habit_name)
    tracker.update_streak()
    tracker.save_to_db(db_path=TEST_DB_PATH)

    loaded = HabitStreakTracker.load_from_db(user_id, habit_name, db_path=TEST_DB_PATH)

    assert loaded.get_streak() == tracker.get_streak()
    assert loaded.last_check_in == tracker.last_check_in
    assert loaded.user_id == tracker.user_id
    assert loaded.habit_name == tracker.habit_name
