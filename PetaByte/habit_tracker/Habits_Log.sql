 CREATE TABLE IF NOT EXISTS Habits_Log(
Habit_ID       INTEGER,
habit_name    TEXT,
last_check_in TEXT,
streak        INTEGER,
points        INTEGER,
resourceUtil text,
cpu_usage integer,
memory_use integer,
disk_use integer,
cpu_temp integer,
timeptr timestamp,
FOREIGN KEY (Habit_ID) REFERENCES Habits(Habit_ID)
            )