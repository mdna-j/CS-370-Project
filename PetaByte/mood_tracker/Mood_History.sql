CREATE TABLE IF NOT EXISTS Mood_History (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    mood TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    source TEXT DEFAULT 'manual', -- 'manual' or 'idle'
    FOREIGN KEY (user_id) REFERENCES Users(Account_ID)
);