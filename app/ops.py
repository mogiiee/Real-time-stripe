from . import models, responses
import sqlite3
from fastapi import HTTPException
from .worker.tasks import (
    create_customer_in_stripe,
    update_customer_in_stripe,
    delete_customer_in_stripe,
)

# from confluent_kafka import Producer


def insert_customer(customer: models.Customer):
    conn = sqlite3.connect("/app/data/database.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (?, ?)",
            (customer.name, customer.email),
        )
        conn.commit()
        customer_id = cursor.lastrowid

        # vonvert Pydantic model to dict and adding local_id for reference
        customer_data = customer.model_dump()
        customer_data["local_id"] = customer_id

        # queue the task for creating a customer in stripe
        create_customer_in_stripe.delay(customer_data)

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

    return responses.response(
        True, "data inserted", data={"name": customer.name, "email": customer.email}
    )


def update_customer(customer_id: int, customer: models.Customer):
    try:
        conn = sqlite3.connect("/app/data/database.db")
        cursor = conn.cursor()

        # Start process
        conn.execute("BEGIN")

        # Check if customer exists and get stripe_customer_id
        cursor.execute(
            "SELECT stripe_customer_id FROM customers WHERE id = ?", (customer_id,)
        )
        customer_record = cursor.fetchone()
        if not customer_record:
            raise HTTPException(status_code=404, detail="Customer not found")

        stripe_customer_id = customer_record[0]

        # Attempt to update customer in the local database
        cursor.execute(
            "UPDATE customers SET name = ?, email = ? WHERE id = ?",
            (customer.name, customer.email, customer_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=400, detail="No changes made")

        # Commit changes
        conn.commit()

        # Prepare customer data for strip update
        customer_data = {
            "name": customer.name,
            "email": customer.email,
            "stripe_customer_id": stripe_customer_id,
        }

        # Call the celery task to update the customer in stripe
        update_customer_in_stripe.delay(customer_data)

    except sqlite3.OperationalError:
        conn.rollback()
        raise HTTPException(
            status_code=503, detail="Database is locked, please try again later"
        )
    finally:
        conn.close()

    return responses.response(True, None, data={ "message": "Customer update in progress"})


def delete_customer(customer_id: int):
    try:
        conn = sqlite3.connect("/app/data/database.db")
        cursor = conn.cursor()

        # geting stripe customer ID before attempting to delete
        cursor.execute(
            "SELECT stripe_customer_id FROM customers WHERE id = ?", (customer_id,)
        )
        record = cursor.fetchone()
        if not record:
            raise HTTPException(status_code=404, detail="Customer not found")
        stripe_customer_id = record[0]

        #  delete the customer locally
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()

        # queue the task to delete the customer in Striupe
        delete_customer_in_stripe.delay(stripe_customer_id)

    except sqlite3.OperationalError:
        conn.rollback()
        raise HTTPException(
            status_code=503, detail="Database is locked, please try again later"
        )
    finally:
        conn.close()

    return responses.response(True, None, data={"message": "Customer deletion process initiated"})
