from fastapi import APIRouter, Request
from app.database.db_core import Database
from app.services.register_email import send_tiffin_provider_registration_email

db = Database()

router = APIRouter()

@router.post("/register")
def register_user(user_info: dict):
    db.insert_data(user_info, table_name="business_details")
    send_tiffin_provider_registration_email(user_info)
    return {"message": "User registered successfully", "user_info": user_info}

# Profile fetch and Update API

@router.get("/dashboard/profile/{user_id}")
def get_user_profile(user_id: int):
    columns = "business_name, description, email, phone_number, address"
    user_profile = db.fetch_data("business_details",columns,filter={"column":"id","value":user_id})
    # print("User profile data:", user_profile)
    return {"user_profile": user_profile[0] if len(user_profile) > 0 else {} }

@router.put("/dashboard/profile/{user_id}")
async def save_user_profile(request: Request, user_id:int):
    data = await request.json()
    print("data received", data)
    filter={"column":"id","value":user_id}
    # columns = "business_name, description, email, phone_number, address"
    response = db.update_data("business_details",data,filter)
    # print("Response:", response )
    return response

# Menu fetch and Update API

@router.get("/dashboard/menu/{user_id}")
def get_menu(user_id:int):
    filter={"column":"service_id","value":user_id}
    response = db.fetch_data("services_menu","items",filter)
    # print("Response",response[0]['items'])
    return response[0]['items']

@router.put("/dashboard/menu/{user_id}")
async def save_menu(request: Request, user_id:int):
    filter={"column":"service_id","value":user_id}
    temp = await request.json()
    data = {"items":{"items": temp}}
    print("Data received:", data)
    response = db.update_data("services_menu",data,filter)
    print("Response from DB",response)

# Extras fetch and Update API
@router.get("/dashboard/extra/{user_id}")
def get_extra(user_id:int):
    filter={"column":"service_id","value":user_id}
    response = db.fetch_data("services_menu","extras",filter)
    # print("Response",response[0]['extras'])
    return response[0]['extras']

@router.put("/dashboard/extra/{user_id}")
async def save_extra(request: Request, user_id:int):
    filter={"column":"service_id","value":user_id}
    temp = await request.json()
    data = {"extras": temp}
    # print("Data received:", data)
    response = db.update_data("services_menu",data,filter)
    print("Response from DB",response)