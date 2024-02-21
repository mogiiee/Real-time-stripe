import sqlite3

def ensure_db_setup():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()