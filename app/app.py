from fastapi import FastAPI, HTTPException, Request, status
from app.database.db_core import Database
from fastapi.middleware.cors import CORSMiddleware
from app.models.model import userData
from app.services.email_service import send_order_confirmation_email
from app.services.telegram_service import send_telegram_order_alert
from app.api import dashboard

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

app.include_router(
    dashboard.router
)

db = Database()

@app.get("/")
def root():
    return ("Welcome to Foodeta backend")

@app.post("/login")
async def login(req: Request):
    data = await req.json()
    username = data['username']
    password = data['password']
    filter={"column":"email","value":username}
    columns = "email, password, id, business_name"
    res = db.fetch_data("business_details",columns,filter)[0]
    email = res['email']
    userpassword = res['password']
    if (email == username and userpassword == password):
        businessid = res['id']
        businessname = res['business_name']
        response = { 'businessid': businessid,
                    'businessname': businessname }
    else :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@app.get("/tiffinlist")
def read_database():
    response = db.fetch_data("foodeta","*")
    # print(response)
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
    db.insert_data(user_db, table_name="user_details")
    send_telegram_order_alert(data)
    # send_order_confirmation_email(data)
    return {"message": "Order placed successfully"}