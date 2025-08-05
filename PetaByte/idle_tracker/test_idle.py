import pytest
from unittest.mock import patch, MagicMock
from idle_tracker.idle import map_mood_from_app, insert_idle_log, track_user_activity


# Setup: Dummy user_id and app/mood data
user_id = 1
timestamp = "12:00:00"
app_name = "chrome.exe"
mood = "lazy"

# Test map_mood_from_app() for Windows and macOS
@patch("platform.system", return_value="Windows")
def test_map_mood_windows(mock_platform):
    assert map_mood_from_app("chrome.exe") == "lazy"
    assert map_mood_from_app("Code.exe") == "productive"
    assert map_mood_from_app("unknown_app.exe") == "neutral"

@patch("platform.system", return_value="Darwin")
def test_map_mood_macos(mock_platform):
    assert map_mood_from_app("Safari") == "lazy"
    assert map_mood_from_app("Xcode") == "productive"
    assert map_mood_from_app("UnknownApp") == "neutral"

# Test database insert
@patch("sqlite3.connect")
def test_insert_idle_log(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    insert_idle_log(user_id, timestamp, app_name, mood)

    mock_cursor.execute.assert_any_call('''
        CREATE TABLE IF NOT EXISTS Idle_Activity_Log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            app_name TEXT,
            mood TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(Account_ID)
        )
    ''')
    mock_cursor.execute.assert_any_call('''
        INSERT INTO Idle_Activity_Log (user_id, timestamp, app_name, mood)
        VALUES (?, ?, ?, ?)
    ''', (user_id, timestamp, app_name, mood))
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch.multiple("idle_tracker.idle",
    insert_idle_log=lambda *a, **kw: None,
    map_mood_from_app=lambda app: "productive",
    get_active_app_name=lambda: "Code.exe",
    log_mood=lambda *a, **kw: None
)
@patch("time.sleep", return_value=None)
def test_track_user_activity(mock_sleep):
    log = track_user_activity(user_id="test_user", duration_sec=1, interval_sec=0.1)
    assert log and log[0][1] == "Code.exe" and log[0][2] == "productive"