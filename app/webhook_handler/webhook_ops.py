import sqlite3


def db_connection():
    """Create and return a database connection."""
    return sqlite3.connect("/app/data/database.db")


def insert_customer(name, email, stripe_customer_id):
    """Insert a new customer into the database."""
    conn = db_connection()
    query = "INSERT INTO customers (name, email, stripe_customer_id) VALUES (?, ?, ?)"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (name, email, stripe_customer_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def update_customer_by_stripe_id(stripe_customer_id, name, email):
    """Update an existing customer in the database by Stripe customer ID."""
    conn = db_connection()
    query = "UPDATE customers SET name = ?, email = ? WHERE stripe_customer_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (name, email, stripe_customer_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def delete_customer_by_stripe_id(stripe_customer_id):
    """Delete a customer from the database by Stripe customer ID."""
    conn = db_connection()
    query = "DELETE FROM customers WHERE stripe_customer_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (stripe_customer_id,))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
