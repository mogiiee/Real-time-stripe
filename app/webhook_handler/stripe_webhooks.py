
from fastapi import APIRouter, Request, HTTPException, status
import stripe
from . import webhook_ops, exporter

router = APIRouter()


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, exporter.stripe_secret_key
        )

    except ValueError as e:
        # Invalid payload
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload :" + str(e)
        )
    except stripe.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature :" + str(e),
        )

    if event["type"] == "customer.created":
        customer = event["data"]["object"]
        handle_customer_created(customer)
    elif event["type"] == "customer.deleted":
        customer = event["data"]["object"]
        handle_customer_deleted(customer)
    elif event["type"] == "customer.updated":
        customer = event["data"]["object"]
        handle_customer_updated(customer)

    return {"status": "success"}


def handle_customer_updated(customer):
    # Logic to handle customer.updated events from Stripe.
    stripe_customer_id = customer.get("id")
    name = customer.get("name")
    email = customer.get("email")
    webhook_ops.update_customer_by_stripe_id(stripe_customer_id, name, email)


def handle_customer_deleted(customer):
    # Logic to handle customer.deleted events from Stripe.
    stripe_customer_id = customer.get("id")
    webhook_ops.delete_customer_by_stripe_id(stripe_customer_id)


def handle_customer_created(customer):
    # Logic to handle customer.deleted events from Stripe.
    stripe_customer_id = customer.get("id")
    name = customer.get("name")
    email = customer.get("email")
    webhook_ops.insert_customer(
        name, email=email, stripe_customer_id=stripe_customer_id
    )
