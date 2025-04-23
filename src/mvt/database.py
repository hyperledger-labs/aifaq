import streamlit as st
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