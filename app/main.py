from fastapi import FastAPI, HTTPException
from .database import ensure_db_setup
from . import models, responses, ops

app = FastAPI()

ensure_db_setup()



@app.post("/customers")
async def create_customer(customer: models.Customer):

    data = ops.insert_customer(customer)
    return  responses.response(True, None, data= data) 

    # raise HTTPException(status_code=400, detail=str(e))
    


@app.put("/update_customers/{customer_id}")
async def update_customers(customer_id,customer: models.Customer):
    try:
        data = ops.update_customer(customer_id, customer)
        return  responses.response(True, None, data= data) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_customers/{customer_id}")
async def delete_customer(customer_id: int):
    try:
        data = ops.delete_customer(customer_id,)
        return  responses.response(True, None, data= data) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))