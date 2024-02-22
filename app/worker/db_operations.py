import sqlite3
from fastapi import HTTPException


def update_local_customer_with_stripe_id(local_id, stripe_customer_id):
    """
    Update the local database record with the Stripe customer ID.
    """
    try:
        conn = sqlite3.connect("/app/data/database.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE customers SET stripe_customer_id = ? WHERE id = ?",
            (stripe_customer_id, local_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Local customer not found")
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409, detail="Conflict with the current state of the resource"
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def remove_local_customer(stripe_customer_id):
    """
    Remove or mark a customer as deleted in the local database by Stripe customer ID.
    """
    try:
        conn = sqlite3.connect("/app/data/database.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM customers WHERE stripe_customer_id = ?", (stripe_customer_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Local customer not found")
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409, detail="Conflict with the current state of the resource"
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
