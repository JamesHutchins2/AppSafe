import subprocess
import threading
import os
import socket
import streamlit as st

MODULES_DIR = "Modules"
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port):
    port = start_port
    while is_port_in_use(port):
        port += 1
        if port > start_port + 100:  # Limit to 100 attempts
            raise Exception("No available ports found in the range.")
    return port

def deploy_app(app_dir):
    make_table_script = os.path.join(app_dir, 'makeTable.py')
    app_script = os.path.join(app_dir, 'application.py')
    info_file_path = os.path.join(app_dir, 'info.txt')

    # Read the port number from info.txt
    with open(info_file_path, 'r') as file:
        for line in file:
            if line.startswith('Port Number:'):
                port = int(line.split(':')[1].strip())
                break
        else:
            raise Exception("Port number not found in info.txt")

    # Find an available port
    port = find_available_port(port)

    # Update the port number in info.txt
    with open(info_file_path, 'w') as file:
        file.write(f"Port Number: {port}\n")

    # Run makeTable.py to set up the database
    subprocess.run(['python', make_table_script])

    # Function to run the Streamlit app
    def run_app():
        subprocess.run(['streamlit', 'run', app_script, '--server.port', str(port)])

    # Run the Streamlit app in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()
    st.success(f"App {os.path.basename(app_dir)} deployed on port {port}")
def main():
    st.title("App Deployment Dashboard")

    # Scan the Modules directory for apps
    app_dirs = [d for d in os.listdir(MODULES_DIR) if os.path.isdir(os.path.join(MODULES_DIR, d))]

    # Create a button for each app
    for app_dir in app_dirs:
        if st.button(f"Deploy {app_dir}"):
            deploy_app(os.path.join(MODULES_DIR, app_dir))

if __name__ == "__main__":
    main()
