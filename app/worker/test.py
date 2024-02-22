
import sqlite3
from fastapi import HTTPException
import stripe
import os
import dotenv

dotenv.load_dotenv()


stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")


print(stripe_secret_key)

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

cus = {
    "name": "John Doe",
    "email": "hi@ex.com",
    "id" : 2
}


def db_connection():
    return sqlite3.connect('mydatabase.db')


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
    
delete_stripe_customer(2)