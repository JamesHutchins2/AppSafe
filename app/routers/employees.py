from fastapi import FastAPI, HTTPException, Depends, APIRouter
from models import pydantic_models as employees
from database import connection as db
import motor.motor_asyncio
import logging
import traceback
from typing import List, Any
import authentication
from database import connection
router = APIRouter()
from pydantic import ValidationError
import ast

# Function for connecting to the Database.
def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    db = client["appsafe_1"]
    return db

#import pydantic models
Employee = employees.Employee
EmployeeCreate = employees.EmployeeCreate


#end point for registering a new employee
@router.post('/employee/register/')
async def create_employee(request: Employee):

    #hash the given password
    hashed_password = authentication.get_password_hash(request.password)
    #Create the employee object from the request infromation
    employee_object = dict(request)
    #apply the hashed password to the employee object
    employee_object["password"] = hashed_password

    #connect to the database
    db = await connection.get_db()
    #insert the employee object into the database
    await db["employees"].insert_one(employee_object)
    return request
    
#end point for deleting an employee, we will need to add admin authentication to this end point


@router.get("/users/me/", response_model=Employee)
async def read_users_me(current_user: Employee = Depends(authentication.get_current_active_user)):
    return current_user

