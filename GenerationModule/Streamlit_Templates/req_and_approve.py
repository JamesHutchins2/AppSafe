import streamlit as st
from mongomock import MongoClient

# Connect to MongoDB
client = MongoClient()
db = client.your_database  # Change 'your_database' to your actual database name
collection = db.requests  # Change 'requests' to your actual collection name

def get_requests_from_database():
    # Fetch requests from the database
    cursor = collection.find({})
    requests = [request for request in cursor]
    return requests

def get_pending_requests():
    # Fetch requests from the database that are not yet approved or declined
    cursor = collection.find({"status": {"$exists": False}})
    pending_requests = [request for request in cursor]
    return pending_requests

def get_approved_and_declined_requests():
    # Fetch all approved and declined requests
    approved_requests = list(collection.find({"status": "Approved"}))
    declined_requests = list(collection.find({"status": "Declined"}))
    return approved_requests, declined_requests

def get_declined_requests_titles_and_descriptions():
    # Fetch titles and descriptions of declined requests
    cursor = collection.find({"status": "Declined"}, {"title": 1, "description": 1, "_id": 0})
    titles_and_descriptions = [{"title": request["title"], "description": request["description"]} for request in cursor]
    return titles_and_descriptions

def get_declined_request_details(title):
    # Fetch details of a specific declined request based on title
    return collection.find_one({"status": "Declined", "title": title})

def request_approval_app(title="Request and Approval Form", 
                         desc="Welcome to the Request and Approval System!"):

    st.title(title)

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Form Description", "Submit Request", "Approve Requests", "View Requests"])

    # Main Content
    if page == "Form Description":
        home_desc(desc)
    elif page == "Submit Request":
        submit_request()
    elif page == "Approve Requests":
        approve_requests()
    elif page == "View Requests":
        view_requests()

def home_desc(desc):

    st.write(desc)

def submit_request():
    st.header("Submit Request")

    # Form for submitting requests
    with st.form("request_form"):
        request_title = st.text_area("Request Title")
        request_description = st.text_area("Request Description")
        submit_button = st.form_submit_button("Submit Request")

    # Process the submitted request
    if submit_button:
        
        request_data = {
            "title": request_title,
            "description": request_description,
        }
        result = collection.insert_one(request_data)

        if result.inserted_id:
            st.success("Request submitted successfully!")
        else:
            st.error("Error submitting the request.")
        

def approve_requests():
    st.header("Approve or Decline Requests")

    # Fetch pending requests
    pending_requests = get_pending_requests()

    # Display the list of pending requests
    st.subheader("Pending Requests:")
    for request in pending_requests:
        st.text(request['title'])

    # Dropdown menu to select a specific request to approve or decline
    selected_request_title = st.selectbox("Select Request to Approve or Decline:", [""] + [request['title'] for request in pending_requests])

    if selected_request_title:
        # Find the selected request
        selected_request = next((request for request in pending_requests if request['title'] == selected_request_title), None)

        if selected_request:
            # Display approval/decline options and text field
            st.text(f'Request Description:\n{selected_request["description"]}')
            approval_status = st.radio("Select approval status:", ["Approve", "Decline"])
            if approval_status == "Decline":
                decline_reason = st.text_area("Reason for Decline:")
            else:
                decline_reason = None

            # Button to submit approval or decline
            if st.button("Submit"):
                # Update the status and decline reason in the MongoDB collection
                updated_status = "Declined" if approval_status == "Decline" else "Approved"
                update_data = {
                    "$set": {"status": updated_status, "decline_reason": decline_reason}
                }
                result = collection.update_one({"title": selected_request_title}, update_data)

                if result.modified_count > 0:
                    st.success(f"Request {approval_status.lower()}d successfully!")
                else:
                    st.error("Error updating the request.")

                st.rerun()
        else:
            st.warning("Selected request not found.")


def view_requests():
    st.header("View All Request Approvals and Declines")

    # Fetch all approved and declined requests
    approved_requests, declined_requests = get_approved_and_declined_requests()

    # Display list of approved requests
    st.subheader("Approved Requests:")
    for request in approved_requests:
        st.text(f"{request['title']} - Approved")

    # Display list of declined requests
    st.subheader("Approved Requests:")
    for request in declined_requests:
        st.text(f"{request['title']} - Declined")

    # Fetch titles and descriptions of declined requests
    declined_titles_and_descriptions = get_declined_requests_titles_and_descriptions()

    # Dropdown menu to select a specific declined request by description
    selected_title = st.selectbox("Select Declined Request:", [""] + [request["title"] for request in declined_titles_and_descriptions])

    if selected_title:
        # Fetch details of the selected declined request based on title
        selected_request = get_declined_request_details(selected_title)
        
        # Display details of the selected declined request
        st.subheader("Details of Selected Declined Request:")
        st.text(f"Title: {selected_request['title']}")
        st.text(f"Description: {selected_request['description']}")
        st.text(f"Status: {selected_request['status']}")
        st.text(f"Decline Reason: {selected_request.get('decline_reason', 'N/A')}")
    else:
        st.info("Select a declined request from the dropdown.")