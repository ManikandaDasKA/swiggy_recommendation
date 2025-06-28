from fastapi import FastAPI,Depends
from typing import * 
from app.database import create_db_and_tables, call_database,insert_data
from app.user.user_router import user_app as user_router
from app.restaurant.router import app as restaurant_router
from app.user_order.order_router import orders_app as orders_router
from app.recommentation.recommentation import rec

app = FastAPI(title="Swiggy_clone")

app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(orders_router)
app.include_router(rec)

@app.on_event("startup")
def create_database():
    call_database()

@app.post("/create_database")
def create_db():
    dbname = create_db_and_tables()
    return {"message": f"Database {dbname} created successfully."}

@app.get("/health_check")
def health_check():
    return {"message":"ok"}

@app.post("/insert_data")
def inserting_data():
    insert_data()
