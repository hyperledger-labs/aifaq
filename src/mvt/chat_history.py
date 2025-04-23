import sqlite3
from datetime import datetime

DB_FILE = "users.db"

# create a SQLite database to store chat history
# and user information
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# create a table to store user information
def save_message(username, role, content):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            'INSERT INTO messages (username, role, content) VALUES (?, ?, ?)',
            (username, role, content)
        )
        conn.commit()

# retrieve chat history for a specific user
# and return it as a list of dictionaries
def get_messages(username):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            'SELECT role, content FROM messages WHERE username = ? ORDER BY timestamp ASC',
            (username,)
        )
        return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
