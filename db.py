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
        VALUES (?, ?, ?)
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

    # 오늘 기록 중 가장 최근 row 가져오기
    cur.execute("""
        SELECT checkin_time, checkout_time
        FROM attendance
        WHERE username = ? AND date = ?
        ORDER BY id DESC
        LIMIT 1
    """, (username, today))

    row = cur.fetchone()
    conn.close()

    # 기록 없음
    if row is None:
        return "Not Attended Now"

    checkin, checkout = row

    # 출근은 했지만 퇴근 기록 없음 → 현재 출근 상태
    if checkin and not checkout:
        return "Now Online"

    # 출근 + 퇴근 기록 → 오프라인 (퇴근 완료)
    if checkin and checkout:
        return "Now Offline"

    return "Not Attended Now"


def get_online_users():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    # 같은 유저의 여러 기록 중 가장 마지막 기록만 고려해야 함
    # 방법: username별로 마지막(id 최대) row만 골라서 조회
    cur.execute("""
        SELECT a.username, a.checkin_time
        FROM attendance a
        INNER JOIN (
            SELECT username, MAX(id) AS max_id
            FROM attendance
            WHERE date = ?
            GROUP BY username
        ) b
        ON a.id = b.max_id
        WHERE a.checkout_time IS NULL OR a.checkout_time = ''
    """, (today,))

    rows = cur.fetchall()
    conn.close()

    return rows

