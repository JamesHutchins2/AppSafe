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

# Function to add a document in a collection
def add_document(db, collection_name: str, document: Dict):
    collection = db[collection_name]
    return collection.insert_one(document).inserted_id

# Database name
db_name = "companyDB"
db = connect_db(mongo_uri, db_name)

# Employee Collection and Schema
employee_table = 'employees'
employee_schema = {
    "Employee_ID": int,
    "Employee_Name": str,
    "Department_ID": int,
    "Joining_Date": datetime,
    "Position": str
}
employee_id = add_document(db, employee_table, employee_schema)

# Department Collection and Schema
department_table = 'departments'
department_schema = {
    "Department_ID": int,
    "Department_Name": str,
    "Manager_ID": int
}
department_id = add_document(db, department_table, department_schema)

# Outputting the created collections and their schemas
print(f"Employee collection created with ID: {employee_id}")
print(f"Employee collection schema: {employee_schema}")
print(f"Department collection created with ID: {department_id}")
print(f"Department collection schema: {department_schema}")
