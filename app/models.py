from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str

# # class CustomerModel(BaseModel):  # Using Pydantic for example
#     name: str
#     email: str
#     service_id: str  # Stripe ID or Salesforce ID
#     # Additional fields...