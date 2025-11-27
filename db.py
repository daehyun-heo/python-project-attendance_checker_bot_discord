import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    # 기존 date + time 구조는 삭제하고 datetime 구조로 통일
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            checkin DATETIME NOT NULL,
            checkout DATETIME
        )
    """)

    conn.commit()
    conn.close()


def check_in(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO attendance (username, checkin)
        VALUES (?, ?)
    """, (username, now_str))

    conn.commit()
    conn.close()
    return now_str



def check_out(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # 날짜 상관 없이 가장 최근 출근 기록 중 미퇴근 상태 찾기
    cur.execute("""
        SELECT id, checkin
        FROM attendance
        WHERE username = ? AND checkout IS NULL
        ORDER BY id DESC
        LIMIT 1
    """, (username,))

    row = cur.fetchone()

    if row is None:
        conn.close()
        return now_str, None  

    record_id, checkin_str = row
    checkin_dt = datetime.strptime(checkin_str, "%Y-%m-%d %H:%M:%S")

    cur.execute("""
        UPDATE attendance
        SET checkout = ?
        WHERE id = ?
    """, (now_str, record_id))

    conn.commit()
    conn.close()

    delta = now - checkin_dt
    sec = int(delta.total_seconds())

    hours = sec // 3600
    minutes = (sec % 3600) // 60
    seconds = sec % 60

    duration_str = f"{hours}시간 {minutes}분 {seconds}초"

    return now_str, duration_str


def get_log(username):
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    start = f"{today} 00:00:00"
    end = f"{today} 23:59:59"

    # 오늘 시간과 겹치는 모든 interval 조회
    cur.execute("""
        SELECT checkin, checkout
        FROM attendance
        WHERE username = ?
            AND checkin <= ?
            AND (checkout IS NULL OR checkout >= ?)
        ORDER BY checkin ASC
    """, (username, end, start))

    rows = cur.fetchall()
    conn.close()

    return rows


def get_logs():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    start = f"{today} 00:00:00"
    end = f"{today} 23:59:59"

    cur.execute("""
        SELECT username, checkin, checkout
        FROM attendance
        WHERE checkin <= ?
          AND (checkout IS NULL OR checkout >= ?)
        ORDER BY username ASC, checkin ASC
    """, (end, start))

    rows = cur.fetchall()
    conn.close()

    result = {}

    for username, checkin, checkout in rows:
        if username not in result:
            result[username] = []
        result[username].append((checkin, checkout))

    return result

