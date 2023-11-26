from typing import Annotated

from fastapi import Depends, FastAPI
from authentication import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from routers import employees
#import authentication
from models.pydantic_models import Token, TokenData, Employee, EmployeeInDB, EmployeeList, EmployeeApplications
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import pydantic_models
from fastapi import HTTPException, status
from database import connection
import authentication as authentication
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import motor.motor_asyncio
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3000",
    "localhost:3000",
]

    

db = connection.get_db()
app = FastAPI()

async def get_db():
    db = await connection.get_db()
    return db


#middleware

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)



@app.post('/login/')
async def login(request: authentication.OAuth2PasswordRequestForm = Depends()):
    db = await connection.get_db()
    user = await authentication.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
                )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
            data={"sub":user.username}, expires_delta=access_token_expires
            )
    return {"access_token": access_token, "token_type": "bearer"}


#import routers
app.include_router(employees.router)
#app.include_router(authentication.router)

@app.post("/token", response_model=authentication.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = await authentication.authenticate_user(db, form_data.username, form_data.password)
    if not user:

        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
                )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
            data={"sub":user.username}, expires_delta=access_token_expires
            )
    return {"access_token": access_token, "token_type": "bearer"}



#authenticated routes

@app.get("/users/me/", response_model=Employee)
async def read_users_me(current_user: Employee = Depends(authentication.get_current_active_user)):
    return current_user

@app.get("/all_employees/", response_model=EmployeeList)
async def get_all_employees(db: AsyncIOMotorClient = Depends(connection.get_db)):
    cursor = db["employees"].find()
    employees_raw = await cursor.to_list(length=100)
    employees = [Employee(**employee) for employee in employees_raw]  # Transform each document
    return {"employees": employees}



@app.get("/get/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, current_user: Employee = Depends(authentication.get_current_active_user)):
    db = await connection.get_db()
    employee = await db["employees"].find_one({"id": employee_id})
    if employee:
        print(employee)  # Debugging line to output the data
        return Employee(**employee)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.get("/get/employees/{username}/applications", response_model=EmployeeApplications)
async def get_employee_applications(username: str, current_user: Employee = Depends(authentication.get_current_active_user)):
    db = await connection.get_db()
    employee = await db["employees"].find_one({"username": username})
    if employee:
        #get the list of application IDs, and the premissions for each application
        app_list = employee["app_list"]
        premissions = employee["premissions"]

        #return the list of applications
        return {"app_list": app_list, "premissions": premissions}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.get("/users/me/applications", response_model=EmployeeApplications)
async def read_users_me_applications(current_user: Employee = Depends(authentication.get_current_active_user)):
    db = await connection.get_db()
    employee = await db["employees"].find_one({"username": current_user.username})
    if employee:
        #get the list of application IDs, and the premissions for each application
        app_list = employee["app_list"]
        premissions = employee["premissions"]

        #return the list of applications
        return {"app_list": app_list, "premissions": premissions}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")