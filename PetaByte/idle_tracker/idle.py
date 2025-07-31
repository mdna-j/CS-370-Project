import platform
import time
import datetime
import sqlite3

# Define mood map
# Windows app-to-mood mapping
windows_app_mood_map = {
    "chrome.exe": "lazy",
    "firefox.exe": "lazy",
    "msedge.exe": "lazy",
    "Code.exe": "productive",
    "notepad.exe": "neutral",
    "explorer.exe": "browsing",
    "Discord.exe": "social",
    "steam.exe": "gaming",
    "vlc.exe": "relaxed",
    "spotify.exe": "relaxed",
    "outlook.exe": "productive",
    "teams.exe": "productive",
    "zoom.exe": "productive",
    "powerpoint.exe": "productive",
    "excel.exe": "productive",
    "word.exe": "productive",
    "leagueoflegends.exe": "gaming",
    "minecraftlauncher.exe": "gaming",
    "valorant.exe": "gaming",
    "epicgameslauncher.exe": "gaming",
    "battle.net.exe": "gaming",
    "photoshop.exe": "creative",
    "aftereffects.exe": "creative",
    "premiere.exe": "creative",
}
# macOS app-to-mood mapping
macos_app_mood_map = {
    "Safari": "lazy",
    "Google Chrome": "lazy",
    "Firefox": "lazy",
    "Finder": "browsing",
    "Xcode": "productive",
    "Terminal": "productive",
    "Notes": "productive",
    "Mail": "productive",
    "Calendar": "productive",
    "Slack": "productive",
    "Zoom": "productive",
    "Microsoft Word": "productive",
    "Microsoft Excel": "productive",
    "Discord": "social",
    "Steam": "gaming",
    "Spotify": "relaxed",
    "Photos": "relaxed",
    "iMovie": "creative",
    "Final Cut Pro": "creative",
    "Photoshop": "creative",
    "League of Legends": "gaming",
    "Minecraft": "gaming",
    "Valorant": "gaming",
}

def get_active_app_name():
    os_type = platform.system()

    if os_type == "Windows":
        try:
            import win32gui, win32process, psutil
        except ImportError:
            return None

        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            return psutil.Process(pid).name()
        except psutil.NoSuchProcess:
            return None

    elif os_type == "Darwin":
        try:
            from AppKit import NSWorkspace
        except ImportError:
            return None

        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return app.localizedName()

    else:
        return None

def map_mood_from_app(app_name):
    os_type = platform.system()

    if os_type == "Windows":
        return windows_app_mood_map.get(app_name, "neutral")
    elif os_type == "Darwin":
        return macos_app_mood_map.get(app_name, "neutral")
    else:
        return "neutral"

def track_user_activity(duration_sec=60, interval_sec=5):
    """
    Runs for `duration_sec`, polling every `interval_sec`.
    Returns a list of (timestamp, app_name, mood) tuples.
    """
    print(f"🔍 Tracking user activity for {duration_sec} seconds...\n")
    end_time = time.time() + duration_sec
    mood_log = []

    while time.time() < end_time:
        app = get_active_app_name()
        mood = map_mood_from_app(app)
        ts = datetime.datetime.now().strftime("%H:%M:%S")

        if app:
            print(f"[{ts}] App: {app}, Mood: {mood}")
            mood_log.append((ts, app, mood))
        else:
            print(f"[{ts}] App: Unknown, Mood: neutral")
            mood_log.append((ts, None, "neutral"))

        time.sleep(interval_sec)

    return mood_log



def insert_idle_log(user_id, timestamp, app_name, mood):
    conn = sqlite3.connect("PetaByte/database/petabyte.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Idle_Activity_Log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            app_name TEXT,
            mood TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(Account_ID)
        )
    ''')
    cursor.execute('''
        INSERT INTO Idle_Activity_Log (user_id, timestamp, app_name, mood)
        VALUES (?, ?, ?, ?)
    ''', (user_id, timestamp, app_name, mood))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Example: track for 30 seconds, polling every 5s
    log = track_user_activity(duration_sec=30, interval_sec=5)
    print("\nCollected activity log:")
    for entry in log:
        print(entry)
