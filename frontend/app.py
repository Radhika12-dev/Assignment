import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/api"

#Session state to store the access token
if 'token' not in st.session_state:
    st.session_state['token'] =''

st.title("🗂️ Task Manager")

#User Registeration
st.header('Register')
username = st.text_input("Username", key="reg_username")
password = st.text_input("Password", type="password", key="reg_password")

if st.button("Register"):
    response = requests.post(f"{API_URL}/register/", json={'username':username, 'password': password})
    if response.status_code == 200:
        st.success("User Registered Successfully.")
    else:
        st.error(f"Registeration failed: {response.json()}")

#User Login
st.header("Login")
login_username = st.text_input("Username", key= "login_username")
login_password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    response = requests.post(f"{API_URL}/login/", json={'username':login_username, 'password': login_password})
    if response.status_code == 200:
        st.session_state['token'] = response.json()['access']
        st.success("Logged in Successfully!")
    else:
        st.error("Login Failed")

#If logged in then show Task Mnager
if st.session_state['token']:
    st.header("Task Manager")
    auth_header = {"Authorization": f"Bearer {st.session_state['token']}"}

    # Create Task
    st.subheader("Create Task")
    title = st.text_input("Task Title")
    description = st.text_input("Task Description")

    if st.button('Add Task'):
        response = requests.post(f'{API_URL}/tasks/',
                                headers=auth_header,
                                json={'title': title, 'description': description})
        
        if response.status_code == 201:
            st.success("Task created successfully!")
        elif response.status_code == 429:
            st.warning("You are making requests too quickly. Please wait and try again later.")
        else:
            st.error("Failed to create task.")

    # Initialize page tracker
    if 'current_page_url' not in st.session_state:
        st.session_state['current_page_url'] = f'{API_URL}/tasks/'

    # Display Tasks with Pagination
    st.subheader("Your Tasks")
    response = requests.get(st.session_state['current_page_url'], headers=auth_header)

    if response.status_code == 200:
        data = response.json()
        tasks = data['results']

        if tasks:
            # Display the table
            task_data = []
            for task in tasks:
                task_data.append({
                    'ID': task['id'],
                    'Title': task['title'],
                    'Description': task['description'],
                    'Completed': "✅" if task['completed'] else "❌"
                })

            df = pd.DataFrame(task_data)
            st.dataframe(df)

            # Pagination Controls
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            with nav_col1:
                if data['previous']:
                    if st.button('⬅️ Previous Page'):
                        st.session_state['current_page_url'] = data['previous']
                        

            with nav_col3:
                if data['next']:
                    if st.button('Next Page ➡️'):
                        st.session_state['current_page_url'] = data['next']
                        

        else:
            st.info("No tasks found.")
    elif response.status_code == 429:
        st.warning("You are making requests too quickly. Please wait and try again later.")
    else:
        st.error("Failed to fetch tasks.")

 

    # Task selection and management
    if response.status_code == 200 and tasks:
        task_titles = [task['title'] for task in tasks]
        selected_title = st.selectbox("Select a task to manage:", task_titles)

        selected_task = next(task for task in tasks if task['title'] == selected_title)

        st.write(f"### Selected Task: {selected_task['title']}")
        st.write(f"**Description:** {selected_task['description']}")
        st.write(f"**Completed:** {'✅' if selected_task['completed'] else '❌'}")

        col1, col2 = st.columns(2)
        if col1.button("✅ Mark as Complete"):
            update_response = requests.put(f"{API_URL}/tasks/{selected_task['id']}",
                                        headers=auth_header,
                                        json={"completed": True})

            if update_response.status_code == 200:
                st.success(f"Task '{selected_task['title']}' marked as completed!")
                st.experimental_rerun()
            else:
                st.error("Failed to update task.")

        if col2.button("🗑️ Delete Task"):
            delete_response = requests.delete(f"{API_URL}/tasks/{selected_task['id']}", headers=auth_header)

            if delete_response.status_code == 204:
                st.success(f"Task '{selected_task['title']}' deleted successfully!")
                st.experimental_rerun()
            else:
                st.error("Failed to delete task.")
