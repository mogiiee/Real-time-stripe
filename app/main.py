from fastapi import FastAPI, HTTPException
import sqlite3
from .database import ensure_db_setup
from . import models, responses


app = FastAPI()

ensure_db_setup()



@app.post("/customers/")
async def create_customer(customer: models.Customer):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (customer.name, customer.email))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()
    return  responses.response(True, 
                               "data inserted", 
                               data= {"name": customer.name, "email": customer.email} 
                               ) 
