import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT NOT NULL,
            checkin_time TEXT,
            checkout_time TEXT
        )
    """)
    conn.commit()
    conn.close()

def check_in(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    cur.execute("""
        INSERT INTO attendance (username, date, checkin_time)
        VALUES (?, ?, ?, ?)
    """, (username, today, now))

    conn.commit()
    conn.close()

def check_out(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    cur.execute("""
        UPDATE attendance
        SET checkout_time = ?
        WHERE username = ? AND date = ?
    """, (now, username, today))

    conn.commit()
    conn.close()

def get_status(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""
        SELECT checkin_time, checkout_time
        FROM attendance
        WHERE username = ? AND date = ?
        ORDER BY id DESC
        LIMIT 1
    """, (username, today))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return "Not Attended"

    checkin, checkout = row
    
    if checkin and not checkout:
        return "Now Online"

    if checkin and checkout:
        return "Now Offline"

    return "Not Attended"
