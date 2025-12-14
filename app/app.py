from fastapi import FastAPI, Request
from app.database.db_core import Database
from fastapi.middleware.cors import CORSMiddleware
# from app.services.email_service import send_order_confirmation_email
from app.services.telegram_service import send_telegram_order_alert

app = FastAPI()

origins = [
        "http://localhost:4200",  # Example: your frontend running on localhost
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies, authorization headers, etc.
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in the request
    )

@app.get("/")
def root():
    return ("Welcome to Foodeta backend")

@app.get("/database")
def read_database():
    db = Database()
    response = db.execute_query()
    return response

@app.post("/place-order")
async def place_order(request: Request):
    data = await request.json()
    print("Order received:", data)
    send_telegram_order_alert(data)
    # send_order_confirmation_email(data)
    return {"message": "Order placed successfully"}