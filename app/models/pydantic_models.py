from pydantic import BaseModel
from typing import List, Any

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


class Application(BaseModel):
    id: int
    container_name: str
    container_description: str
    container_endpoint: str
    container_port: int
    container_image: str




class EmployeeCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    app_list: List[int] # the application ids (values from 0 to 3)
    premissions: List[str] # the premissions for each application either "R", "W", or "A"
    

class Login(BaseModel):
    username: str 
    password: str
    


class Employee(EmployeeCreate):
    id: int
    password: str    
    first_name: str
    last_name: str
    username: str
    
    
    

class EmployeeInDB(Employee):
    password: str
    
    
    
    

class EmployeeList(BaseModel):
    employees: List[Employee]



class EmployeeApplications(BaseModel):
    app_list: List[int]
    premissions: List[str]