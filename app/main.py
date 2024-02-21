from fastapi import FastAPI, HTTPException
from .database import ensure_db_setup
from . import models, responses, ops


app = FastAPI()

ensure_db_setup()



@app.post("/customers/")
async def create_customer(customer: models.Customer):
    try:
        data = ops.insert_customer(customer)
        return  responses.response(True, None, data= data) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
