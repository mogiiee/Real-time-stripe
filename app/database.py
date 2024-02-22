import sqlite3


def ensure_db_setup():
    conn = sqlite3.connect("/app/data/database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL ,
        stripe_customer_id TEXT UNIQUE
);

    """
    )
    conn.commit()
    conn.close()
