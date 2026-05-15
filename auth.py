import sqlite3
import hashlib
import os
import streamlit as st

DB_PATH = "data/users.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

def register_user(name, email, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE email = ? AND password = ?",
              (email, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def is_logged_in():
    return st.session_state.get("logged_in", False)

def get_username():
    return st.session_state.get("username", "")

def do_login(name):
    st.session_state["logged_in"] = True
    st.session_state["username"]  = name

def do_logout():
    st.session_state["logged_in"] = False
    st.session_state["username"]  = ""