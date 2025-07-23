CREATE TABLE IF NOT EXISTS Users (
    Account_ID INTEGER PRIMARY KEY autoincrement ,
    Username TEXT NOT NULL UNIQUE,
    Contact_Email TEXT

);

