from fastapi import FastAPI
from app.database.db_core import Database
from fastapi.middleware.cors import CORSMiddleware

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