from typing import Annotated

from fastapi import Depends, FastAPI

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

#import authentication
from models.pydantic_models import Token, TokenData, Employee, EmployeeInDB
from database import connection

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import pydantic_models
from fastapi import HTTPException, status

# Security protocols
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



#security intialization
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




#Verify that the plain password, and hashed password match
def verify_password(plain_password, hashed_password):
    
    
    # * This will have to be fixed (need to store the hashed passwords in db)
    hashed_password = get_password_hash(hashed_password)
    
    received_hash = get_password_hash(plain_password)
    

    return pwd_context.verify(plain_password, hashed_password)


#hash the password
def get_password_hash(password):
    return pwd_context.hash(password)


#get's an employee from the database
async def get_user(db, username: str):
    
    #fetch the user from the database
    db = await connection.get_db()
    user_dict = await db["employees"].find_one({"username": username})
    if user_dict:
        return EmployeeInDB(**user_dict)
    else:
        return None
    
#get's the employee, and ensure that the password is correct
async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    print(f"Provided Password: {password}")
    print(f"Stored Hashed Password: {user.password}")
    if not verify_password(password, user.password):
        return False
    return user

# Creates a JWT token
def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#get the current user
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(connection.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: int = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


#ensure that the user is active
async def get_current_active_user(current_user: Employee = Depends(get_current_user)):
    
    return current_user






