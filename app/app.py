from fastapi import FastAPI, Request
from app.database.db_core import Database
from fastapi.middleware.cors import CORSMiddleware
from app.models.model import userData
from app.services.email_service import send_order_confirmation_email
from app.services.telegram_service import send_telegram_order_alert

app = FastAPI()

origins = [
        "http://localhost:4200",  # frontend running on localhost
        "https://foodeta-ui-1030483456536.northamerica-northeast2.run.app/",
        "https://foodeta-ui-1030483456536.northamerica-northeast2.run.app",
        r"^https:\/\/foodeta.*\.run.app\/?$"  # deployed frontend URL
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
    # print("Order received:", data)
    # print("User Details:", data.get("customerInfo"))
    user_db:userData={
        "name":data.get("customerInfo")["fullName"],
        "email":data.get("customerInfo")["email"],
        "phone":data.get("customerInfo")["phone"],
        "address":data.get("customerInfo")["address"],
    }
    # print("User DB:", user_db)
    db= Database()
    db.insert_data(user_db)
    send_telegram_order_alert(data)
    # send_order_confirmation_email(data)
    return {"message": "Order placed successfully"}