# TASK MANAGER APPLICATION 

A full-stack Task Manager that enables users to register, log in, create, view, update, and delete tasks with real-time visual summaries. Built using Django REST Framework for the backend and Streamlit for the frontend, the application supports JWT authentication, pagination, throttling, and provides interactive charts.

# FEATURES 
1. User Registration and JWT Login
2.  Create, Read, Update, Delete (CRUD) Tasks
3. Mark Tasks as Completed
4. Pagination (3 Tasks Per Page)
5. Global Throttling: 5 Requests Per Minute Per User
6. UI Throttling Warnings
7. Streamlit Interactive Frontend

# TECH STACK

1. Backend: Django, Django REST Framework
2. Frontend: Streamlit
3. Authentication: JWT (Simple JWT)
4. Visualization: Matplotlib
5. Database: SQLite (default)

# SETUP INSTRUCTIONS

1. Clone the Repository
       - git clone https://github.com/Radhika12-dev/Assignment.git
       - cd task_manager

2. Create and Activate Virtual Environment
        - python -m venv env
        - source env/bin/activate

3. Install Requirements
        - pip install -r requirements.txt

4. Run Migrations
        - python manage.py migrate

5. Start Django Server
        - python manage.py runserver

6. Start Streamlit Frontend
        - cd frontend
        - streamlit run app.py

7. Running Tests
        - python manage.py tests
