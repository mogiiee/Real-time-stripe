import stripe
from . import exporter
from fastapi import HTTPException
import sqlite3


stripe.api_key = exporter.stripe_secret_key


# Set your secret key: remember to change this to your live secret key in production

def db_connection():
    return sqlite3.connect('mydatabase.db')

def create_stripe_customer(customer_data):
    try:
        # Create a customer in Stripe
        stripe_customer = stripe.Customer.create(
            name=customer_data['name'],
            email=customer_data['email'],
            description="Customer for {0}".format(customer_data['name']),
        )
        return stripe_customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_stripe_customer(customer_id, customer_data):
    try:
        # Fetch the corresponding Stripe customer ID from your database
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stripe_customer_id FROM customers WHERE id = ?", (customer_id,))
        stripe_customer_id = cursor.fetchone()
        if not stripe_customer_id:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Update the customer in Stripe
        stripe_customer = stripe.Customer.modify(
            stripe_customer_id[0],
            name=customer_data['name'],
            email=customer_data['email'],
        )
        conn.close()
        return stripe_customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_stripe_customer(customer_id):
    try:
        # Fetch the corresponding Stripe customer ID from your database
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stripe_customer_id FROM customers WHERE id = ?", (customer_id,))
        stripe_customer_id = cursor.fetchone()
        if not stripe_customer_id:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Delete the customer in Stripe
        stripe.Customer.delete(stripe_customer_id[0])
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
