-- schema.sql

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content BLOB NOT NULL,
    hash TEXT NOT NULL
);
