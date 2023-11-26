from pymongo import MongoClient
from getpass import getpass
import streamlit as st
from datetime import datetime

# Connect to MongoDB
client = MongoClient("<Your MongoDB Connection String>")
db = client['Your Database Name']
users_collection = db['users']
requests_collection = db['requests']

# App
def app():
    
    st.title('IT Request Portal')
    
    login_option = st.sidebar.selectbox('Login As', ['Worker', 'IT Department'])
    
    
    if login_option == 'Worker':
        st.header('Worker Dashboard')
        username = st.text_input("Username")
        password = getpass()
        if st.button("Login"):
            user = verify_credentials(username, password, 'Worker')
            if user:
                st.success(f"Welcome {username}!")
                menu_option = st.sidebar.selectbox('Options', ['Submit a Request', 'View My Requests'])
                if menu_option == 'Submit a Request':
                    problem = st.textarea("Description of Problem")
                    if st.button("Submit"):
                        request = {
                            "category": problem,
                            "user_id": user['user_id'],
                            "status": "Pending"
                            "timestamp": datetime.now(),
                        }
                        requests_collection.insert_one(request)
                        st.success("Request submitted successfully!")
                        
                elif menu_option == 'View My Requests':
                    my_requests = list(requests_collection.find({"user_id": user['user_id']}))
                    for req in my_requests:
                        st.write(req)

                
    elif login_option == 'IT Department':
        st.header('IT Dashboard')
        password = getpass()
        if st.button("Enter"):
            if password == '<Your IT Department Password>':
                st.success("Access granted!")
                request_cursor = requests_collection.find({})
                for req in request_cursor:
                    status = st.selectbox('Status', ['Pending', 'Underway', 'Complete'])
                    if st.button(f"Update {req['_id']}"):
                        requests_collection.update_one({"_id": req['_id']}, {"$set": {"status": status}})
                        st.success("Status updated successfully!")
            else:
                st.error("Access denied!")

def verify_credentials(username, password, user_type):
    user = users_colletion.find_one({"username": username, "password": password, "user_type": user_type})
    return user

                   
if __name__ == "__main__":
    app()