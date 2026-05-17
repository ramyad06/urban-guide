import sqlite3

DB = "shotme.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            click_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
