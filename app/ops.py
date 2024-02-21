from . import models, responses
import sqlite3
from fastapi import HTTPException



def insert_customer(customer: models.Customer):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (customer.name, customer.email))
        conn.commit()
        customer_id = cursor.lastrowid
        # enqueue_customer_sync("create", customer_id, customer.model_dump())

    except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already exists")
    finally:
            conn.close()
    return  responses.response(True, 
                                "data inserted", 
                                data= {"name": customer.name, "email": customer.email} 
                                ) 


def update_customer(customer_id: int, customer: models.Customer):
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        
        # Start transaction
        conn.execute('BEGIN')
        
        # Check if customer exists
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Attempt to update customer
        cursor.execute("UPDATE customers SET name = ?, email = ? WHERE id = ?", (customer.name, customer.email, customer_id))
        if cursor.rowcount == 0:
            # If no rows were updated, it means no changes were made to the data
            raise HTTPException(status_code=400, detail="No changes made")

        # Commit changes
        conn.commit()
    except sqlite3.OperationalError as e:
        # Rollback in case the database is locked or any other operational error occurs
        conn.rollback()
        raise HTTPException(status_code=503, detail="Database is locked, please try again later")
    except HTTPException as e:
        # For HTTPExceptions raised above, rollback and re-raise the same exception
        conn.rollback()
        raise e
    finally:
        # Ensure the database connection is always closed
        conn.close()
        return responses.response(True, "data updated", data= {"name": customer.name, "email": customer.email} )
    

def delete_customer(customer_id: int):
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        
        # Start transaction
        conn.execute('BEGIN')
        
        # Check if customer exists before attempting to delete
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Attempt to delete the customer
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        if cursor.rowcount == 0:
            # If no rows were deleted, it means the customer could not be found
            raise HTTPException(status_code=404, detail="Customer not found - unable to delete")

        # Commit changes
        conn.commit()
    except sqlite3.OperationalError:
        # Rollback in case the database is locked or any other operational error occurs
        conn.rollback()
        raise HTTPException(status_code=503, detail="Database is locked, please try again later")
    except HTTPException as e:
        # For HTTPExceptions raised above, rollback and re-raise the same exception
        conn.rollback()
        raise e
    finally:
        # Ensure the database connection is always closed
        conn.close()

    # Proceed to enqueue the delete for syncing with Stripe, if necessary
    # enqueue_customer_delete(customer_id)
    
    return responses.response(True, "deleted" , {"message": "Customer deleted successfully", "id": customer_id})