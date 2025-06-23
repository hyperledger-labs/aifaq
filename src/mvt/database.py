import sqlite3

# This script creates a SQLite database to store user information.
# It includes functions to create a connection to the database, create a table for users,
# insert a new user, update user information, and retrieve user data.
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    username text NOT NULL UNIQUE,
                    email text NOT NULL UNIQUE,
                    type text DEFAULT 'guest',
                    user_group text,
                    email_verified integer DEFAULT 0
                );'''
        conn.cursor().execute(sql)
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

def create_prompts_table(conn):
    """Create a table to store system and query rewriting prompts"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS prompts (
                    id integer PRIMARY KEY,
                    prompt_type text NOT NULL,
                    prompt_value text NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );'''
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def save_prompt(conn, prompt_type, prompt_value):
    """Save or update a prompt in the database"""
    try:
        # Check if prompt already exists
        cur = conn.cursor()
        cur.execute("SELECT id FROM prompts WHERE prompt_type = ?", (prompt_type,))
        existing = cur.fetchone()
        
        if existing:
            # Update existing prompt
            sql = '''UPDATE prompts SET prompt_value = ?, updated_at = CURRENT_TIMESTAMP 
                     WHERE prompt_type = ?'''
            cur.execute(sql, (prompt_value, prompt_type))
        else:
            # Insert new prompt
            sql = '''INSERT INTO prompts(prompt_type, prompt_value) VALUES(?,?)'''
            cur.execute(sql, (prompt_type, prompt_value))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error saving prompt: {e}")
        return False

def get_prompt(conn, prompt_type):
    """Retrieve a specific prompt from the database"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT prompt_value FROM prompts WHERE prompt_type = ?", (prompt_type,))
        result = cur.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error retrieving prompt: {e}")
        return None

def get_all_prompts(conn):
    """Retrieve all prompts from the database"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT prompt_type, prompt_value, updated_at FROM prompts ORDER BY prompt_type")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving prompts: {e}")
        return []