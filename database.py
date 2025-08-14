import sqlite3
from utils import load_yaml_file

# Read config data
config_data = load_yaml_file("config.yaml")

# This script creates a SQLite database to store user information.
# It includes functions to create a connection to the database, create a table for users,
# insert a new user, update user information, and retrieve user data.
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config_data["dbpath"])
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    username text NOT NULL UNIQUE,
                    email text NOT NULL UNIQUE,
                    type text DEFAULT 'guest',
                    user_group text,
                    email_verified integer DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );''')

        cursor = conn.execute("PRAGMA table_info(users)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        if "created_at" not in existing_columns:
            conn.execute('ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT now')
        
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# This function creates a new user in the database.
# It takes a connection object, username, email, and type as parameters.
def insert_user(conn, username, email, type):
    sql = '''INSERT INTO users(username, email, type) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (username, email, type))
    conn.commit()
    return cur.lastrowid

# This function updates the user type in the database.
# It takes a connection object, email, and type as parameters.
def update_user_loggedin(conn, email, loggedin):
    sql = '''UPDATE users SET loggedin = ? WHERE email = ?'''
    cur = conn.cursor()
    cur.execute(sql, (loggedin, email))
    conn.commit()

# This function updates the user group in the database.
# It takes a connection object, email, and user group as parameters.
def update_user_email_verified(conn, email, email_verified):
    sql = '''UPDATE users SET email_verified = ? WHERE email = ?'''
    cur = conn.cursor()
    cur.execute(sql, (email_verified, email))
    conn.commit()

# This function retrieves user data from the database.
# It takes a connection object and email as parameters.
def get_user(conn, email):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error during user loading data: {e}")
        return None