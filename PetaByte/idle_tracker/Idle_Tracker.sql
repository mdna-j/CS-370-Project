CREATE TABLE IF NOT EXISTS Idle_Activity_Log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    timestamp TEXT,
    app_name TEXT,
    mood TEXT,
    FOREIGN KEY(user_id) REFERENCES Users(Account_ID)

);