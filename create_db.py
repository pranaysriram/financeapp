import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL,
type TEXT,
category TEXT,
date TEXT,
note TEXT
)
""")

conn.commit()
conn.close()

print("Database created")