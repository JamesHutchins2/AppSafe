import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
#from fastapi_users.db import MongoDBUserDatabase
#from fastapi_users.authentication import CookieAuthentication, JWTAuthentication
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel




# Change data types of columns
fake_employees =  [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password1",
        "app_list": [0, 1, 2, 3],
        "premissions": ["R", "W", "A", "R"],
        "hashed_password": None
    },
    {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "janesmith",
        "password": "password2",
        "app_list": [1, 2, 3],
        "premissions": ["W", "A", "R"],
        "hashed_password": None
    },
    {
        "id": 3,
        "first_name": "Alice",
        "last_name": "Johnson",
        "username": "alicejohnson",
        "password": "password3",
        "app_list": [0, 2],
        "premissions": ["A", "R"],
        "hashed_password": None
    },
    {
        "id": 4,
        "first_name": "Bob",
        "last_name": "Williams",
        "username": "bobwilliams",
        "password": "password4",
        "app_list": [3],
        "premissions": ["R"],
        "hashed_password": None
    },
    {
        "id": 5,
        "first_name": "Eva",
        "last_name": "Brown",
        "username": "evabrown",
        "password": "password5",
        "app_list": [0, 1],
        "premissions": ["W", "A"],
        "hashed_password": None
    },
    {
        "id": 6,
        "first_name": "David",
        "last_name": "Lee",
        "username": "davidlee",
        "password": "password6",
        "app_list": [2, 3],
        "premissions": ["R", "W"],
        "hashed_password": None
    },
    {
        "id": 7,
        "first_name": "Grace",
        "last_name": "Davis",
        "username": "gracedavis",
        "password": "password7",
        "app_list": [0, 1, 2],
        "premissions": ["A", "R", "W"],
        "hashed_password": None
        
    },
    {
        "id": 8,
        "first_name": "Frank",
        "last_name": "Clark",
        "username": "frankclark",
        "password": "password8",
        "app_list": [1],
        "premissions": ["R"],
        "hashed_password": None
        
    },
    {
        "id": 9,
        "first_name": "Helen",
        "last_name": "White",
        "username": "helenwhite",
        "password": "password9",
        "app_list": [2],
        "premissions": ["W"],
        "hashed_password": None
        
    },
    {
        "id": 10,
        "first_name": "George",
        "last_name": "Taylor",
        "username": "georgetaylor",
        "password": "password10",
        "app_list": [3],
        "premissions": ["A"],
        "hashed_password": None
        
    }
]


#now we need to hash the passwords
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def hash_password(password):
    return pwd_context.hash(password)

#hash the passwords, and add them to the fake employees hashed_password field

for employee in fake_employees:
    employee["hashed_password"] = hash_password(employee["password"])



def create_collections():
    DB_URL = "mongodb://admin:password@localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(
        DB_URL,
        server_api=ServerApi('1'),
        uuidRepresentation="standard"
    )

    db = client["appsafe_1"]
    
    # Create collections (tables)
    collections = ["employees", "applications"]
    for collection_name in collections:
        db[collection_name]
    
    #insert fake data
    db["employees"].insert_many(fake_employees)


    print("Database and collections created successfully")

if __name__ == "__main__":
    create_collections()






#let's create some tables



