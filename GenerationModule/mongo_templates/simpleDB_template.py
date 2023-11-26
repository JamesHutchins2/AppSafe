from pymongo import MongoClient
from datetime import datetime
from typing import Dict

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/"

# Function to connect to the database
def connect_db(uri: str, db_name: str):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# Function to create a data entry in a collection
def create_data_entry(db, collection_name: str, data: Dict):
    collection = db[collection_name]
    return collection.insert_one(data).inserted_id

# Function to add a collection with a specific schema
def add_table(db, table_name: str, data_schema: Dict):
    collection = db[table_name]
    return collection.insert_one(data_schema).inserted_id

            # Database name
db_name = "userDB"
db = connect_db(mongo_uri, db_name)

# Collection and schema for Requests
requests_table = 'requests'
requests_schema = {
    "Request_ID": int,
    "Request_Title": str,
    "Request_Description": str,
    "Created_Date": datetime,
    "Request_Status": str
}
equests_table_id = add_table(db, requests_table, requests_schema)

            # Collection and schema for Users
users_table = 'users'
users_schema = {
                "User_ID": int,
                "User_Type": str, # worker/IT
                "User_Name": str
}
users_table_id = add_table(db, users_table, users_schema)
# Outputting the created tables and their schemas
print(f"Requests table created with ID: {requests_table_id}")
print(f"Requests table schema: {requests_schema}")
print(f"Users table created with ID: {users_table_id}")
print(f"Users table schema: {users_schema}")