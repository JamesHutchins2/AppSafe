from pymongo import MongoClient
from datetime import datetime

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/"

# Function to connect to the database
def connect_db(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# Connect to the Database
db_name = "serviceDB"
db = connect_db(mongo_uri, db_name)

# Example Document for Request Collection
request_document = {
    "Request_ID": 1,
    "Request_Title": "Sample Request",
    "Request_Description": "This is a sample request description.",
    "Created_Date": datetime.now(),
    "Request_Status": "Open",
    "Requester_ID": 123,
    "ITHandler_ID": 456
}

# Function to add a document in a collection
def add_document(db, collection_name, document):
    collection = db[collection_name]
    return collection.insert_one(document).inserted_id

# Insert Document into Request Collection
request_id = add_document(db, 'requests', request_document)
print(f"Request collection document inserted with ID: {request_id}")
