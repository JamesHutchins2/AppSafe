# Python full code as required


import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

client = MockMongoClient()

db = client.mydatabase
collection = db.mycollection
last_updated = 0

def add_data_component():
    st.header("Add Data")
    name = st.text_input("Name:")
    desc = st.text_input("Description:")
    if st.button("Add"):
        add_data({"name": name, "desc": desc})
        st.success("Data added successfully!")
        st.rerun()

def view_data_component():
    st.header("View Data")
    data = view_data()
    for item in data:
        name = item.get('name', 'N/A')
        desc = item.get('desc', 'N/A')
        st.write(f"Name: {name}, Description: {desc}")
        st.button(f"Remove {item['_id']}", key=item['_id'])

def remove_data_component():
    st.header("Remove Data")
    remove_by_name = st.checkbox("Remove by Name")
    if remove_by_name:
        name_to_remove = st.text_input("Enter Name to remove:")
        if st.button("Remove"):
            remove_data_by_name(name_to_remove)
            st.success(f"Data with Name '{name_to_remove}' removed successfully!")
            st.rerun()
    else:
        object_id_to_remove = st.text_input("Enter Object ID to remove:")
        if st.button("Remove"):
            remove_data_by_id(object_id_to_remove)
            st.success("Data removed successfully!")
            st.rerun()

def add_data(data):
    collection.insert_one(data)

def view_data():
    return list(collection.find())

def remove_data_by_id(object_id):
    collection.delete_one({"_id": ObjectId(object_id)})

def remove_data_by_name(name):
    collection.delete_many({"name": name})

def run():
    global last_updated

    st.title("MongoDB Database Viewer")
    option = st.sidebar.selectbox("Select Option", ["Add Data", "View Data", "Remove Data"])
    if option == "Add Data":
        add_data_component()
    elif option == "View Data":
        view_data_component()
    elif option == "Remove Data":
        remove_data_component()
    last_updated = collection.count_documents({})

if __name__ == "__main__":
    run()
