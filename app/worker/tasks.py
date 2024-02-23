import stripe
from . import exporter, db_operations
import sqlite3
from .celery_worker import app
from celery import Celery


stripe.api_key = exporter.stripe_secret_key


# Set your secret key:


def db_connection():
    return sqlite3.connect("/app/data/database.db")


app = Celery("tasks", broker="pyamqp://guest@rabbitmq//")
app.config_from_object("app.worker.celery_config")


@app.task
def create_customer_in_stripe(customer_data):
    local_id = customer_data.pop("local_id")
    try:
        stripe_customer = stripe.Customer.create(**customer_data)
        stripe_customer_id = stripe_customer["id"]
        # Update the local database with the Stripe customer ID
        db_operations.update_local_customer_with_stripe_id(local_id, stripe_customer_id)
    except Exception as e:
        print(f"Failed to create Stripe customer: {e}")


@app.task
def update_customer_in_stripe(customer_data):
    stripe_customer_id = customer_data["stripe_customer_id"]
    try:
        del customer_data["stripe_customer_id"]

        # Update the customer in Stripe
        stripe.Customer.modify(stripe_customer_id, **customer_data)
    except stripe.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Error updating customer in Stripe: {e}")


@app.task
def delete_customer_in_stripe(stripe_customer_id):
    try:
        # Delete customer in Stripe
        stripe.Customer.delete(stripe_customer_id)
        db_operations.remove_local_customer(stripe_customer_id)
    except stripe.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Error deleting customer: {e}")
