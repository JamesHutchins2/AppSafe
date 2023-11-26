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
db_name = "retailDB"
db = connect_db(mongo_uri, db_name)

# Product Collection and Schema
product_table = 'products'
product_schema = {
    "Product_ID": int,
    "Product_Name": str,
    "Price": float,
    "Category": str
}
product_id = add_document(db, product_table, product_schema)

# Order Collection and Schema
order_table = 'orders'
order_schema = {
    "Order_ID": int,
    "Product_ID": int,
    "Quantity": int,
    "Order_Date": datetime,
    "Customer_ID": int
}
order_id = add_document(db, order_table, order_schema)

# Outputting the created collections and their schemas
print(f"Product collection created with ID: {product_id}")
print(f"Product collection schema: {product_schema}")
print(f"Order collection created with ID: {order_id}")
print(f"Order collection schema: {order_schema}")
