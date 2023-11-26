from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
#from fastapi_users.db import MongoDBUserDatabase
#from fastapi_users.authentication import CookieAuthentication, JWTAuthentication
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

async def get_db():
    DB_URL = "mongodb://admin:password@localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(
        DB_URL,
        server_api=ServerApi('1'),
        uuidRepresentation="standard"
    )

    db = client["appsafe_1"]

    return db

