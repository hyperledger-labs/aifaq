import sqlite3
import streamlit as st
from utils import load_yaml_file

# Read config data
config_data = load_yaml_file("config.yaml")

DB_FILE = config_data["dbpath"]

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
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback INTEGER DEFAULT NULL
            )
        ''')
        
        cursor = conn.execute("PRAGMA table_info(messages)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        if "feedback" not in existing_columns:
            conn.execute('ALTER TABLE messages ADD COLUMN feedback INTEGER DEFAULT NULL')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                sql_query TEXT NULL,
                options TEXT NULL,
                notes TEXT NULL
            )
        ''')

        conn.commit()

# create a table to store user information
def save_message(username, role, content):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            'INSERT INTO messages (username, role, content) VALUES (?, ?, ?)',
            (username, role, content)
        )
        conn.commit()
        return cursor.lastrowid  # <- Restituisce l'ID generato dall'autoincrement


# retrieve chat history for a specific user
# and return it as a list of dictionaries
def get_messages(username):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            'SELECT id, role, content, feedback FROM messages WHERE username = ? ORDER BY timestamp ASC',
            (username,)
        )
        return [{"id": row[0], "role": row[1], "content": row[2], "feedback": row[3]} for row in cursor.fetchall()] 

def update_feedback(message_id, feedback):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            'UPDATE messages SET feedback = ? WHERE id = ?',
            (feedback, message_id)
        )
        conn.commit()

def on_feedback_change(message_id, fb_key):
    feedback = st.session_state[fb_key]
    update_feedback(message_id, feedback)

def get_feedback(message_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            'SELECT feedback FROM messages WHERE id = ?',
            (message_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else None


