import streamlit as st
import uuid
from datetime import date, datetime, time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time as sleep_time  # To avoid confusion with datetime.time


st.set_page_config(initial_sidebar_state="collapsed")

# -------------------------------
# Users dictionary
# -------------------------------
users = {
    "Waleed": {
        "password": "1234",
        "email": "wellygr77@gmail.com"
    },
    "Abdullah": {
        "password": "12345",
        "email": "3abdullah.cx@gmail.com"
    },
    "Shaden": {
        "password": "123456",
        "email": "shadeeenalturkiii@gmail.com"
    },
    "Hussah": {
        "password": "1234567",
        "email": "hussah.hussa@gmail.com",
        "projects": {
            1: {
                "name": "Employee Attrition Prediction",
                "subject": "Machine Learning",
                "marks": 95,
                "deadline": "2025-04-28",
                "description": "Building a model to predict employee attrition using scikit-learn.",
                "status": "In Progress"
            },
            2: {
                "name": "Solar Energy Analysis",
                "subject": "Data Science",
                "marks": 100,
                "deadline": "2025-04-27",
                "description": "A project analyzing solar energy usage using Python and Power BI.",
                "status": "In Progress"
            }
        }
    }
}

def check_midnight_and_send_emails():
    """Check if current time is midnight and send reminder emails if it is."""
    now = datetime.now()
    midnight = time(0, 0)  # 12:00 AM
    
    # Check if current time is between 00:00:00 and 00:00:59
    if now.time().hour == midnight.hour and now.time().minute == midnight.minute:
        send_reminder_emails()
        # Sleep for 61 seconds to prevent multiple sends in the same minute
        sleep_time.sleep(61)

def send_reminder_emails():
    sender_email = "project1.tuwaiq.bootcamp@gmail.com"
    password = "pdyc kmxj uxfd cscs"
    today = datetime.today()

    for username, user_info in users.items():
        email = user_info.get("email", "")
        projects = user_info.get("projects", {})

        if not email:
            continue
        if not projects:
            continue

        for project_id, project in projects.items():
            project_name = project["name"]
            deadline_str = project["deadline"]
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            days_left = (deadline - today).days

            if days_left < 2:
                message = MIMEMultipart("alternative")
                message["Subject"] = f"Reminder: Project '{project_name}' is due soon!"
                message["From"] = sender_email
                message["To"] = email

                body = f"""
Hello {username},

Just a quick reminder: your project **{project_name}** is due in 2 days (on {deadline_str}).

Good luck!
"""
                message.attach(MIMEText(body, "plain"))

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, email, message.as_string())
                except Exception as e:
                    pass

# Call the function to check time and send emails
check_midnight_and_send_emails()

## Start session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "email" not in st.session_state:
    st.session_state.email = ""
if "in_progress" not in st.session_state:
    st.session_state.in_progress = {}
if "completed" not in st.session_state:
    st.session_state.completed = {}
if "show_project_form" not in st.session_state:
    st.session_state.show_project_form = False
if "editing_project_key" not in st.session_state:
    st.session_state.editing_project_key = None
if "sort_option" not in st.session_state:
    st.session_state.sort_option = "Default"


def login_page():
    st.title("🔐 Trackify")
    st.markdown("### Your projects Tracker 🤩!")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.email = users[username]["email"]  # Fetch stored email if needed

            # Load user projects if any
            if "projects" in users[username]:
                for project_id, project in users[username]["projects"].items():
                    uid = str(uuid.uuid4())
                    st.session_state.in_progress[uid] = project

            if username not in st.session_state.user_data:
                st.session_state.user_data[username] = []
            
            # Use st.rerun() to immediately show the main page
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

def main_page():
    st.title(f"Welcome to Trackify, {st.session_state.username}!")

    # Add Project Button
    if st.button("➕ Add New Project"):
        st.session_state.show_project_form = True
    
    # Project Form (appears as popup when button is clicked)
    if st.session_state.show_project_form:
        with st.form("add_project_form"):
            if st.session_state.editing_project_key:
                project = st.session_state.in_progress[st.session_state.editing_project_key]
                project_name = project["name"]
                subject = project["subject"]
                marks = project["marks"]
                deadline = project["deadline"]
                description = project["description"]
            else:
                project_name = ""
                subject = ""
                marks = 0
                deadline = date.today()
                description = ""

            st.subheader("Add or Edit Project")

            project_name = st.text_input("Project Name", value=project_name, key="project_name")
            subject = st.text_input("Subject", value=subject, key="subject")
            marks = st.number_input("Marks", min_value=0, max_value=100, value=marks, key="marks")
            deadline = st.date_input("Deadline", value=deadline, key="deadline")
            description = st.text_area("Description", value=description, key="description")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Submit"):
                    # new values the user entered
                    project_data = {
                        "name": project_name,
                        "subject": subject,
                        "marks": marks,
                        "deadline": deadline,
                        "description": description,
                        "status": "In Progress"
                    }
                    # update the old project with the new information
                    if st.session_state.editing_project_key:
                       st.session_state.in_progress[st.session_state.editing_project_key] = project_data
                    else:
                        new_key = str(uuid.uuid4())
                        st.session_state.in_progress[new_key] = project_data

                    # Always hide the form and reset after Submit, whether Add or Edit
                    st.session_state.show_project_form = False
                    st.session_state.editing_project_key = None
                    st.rerun()

            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_project_form = False
                    st.session_state.editing_project_key = None
                    st.rerun()

    # Sort options
    st.header("Your Projects")
    sort_option = st.selectbox(
        "Sort by:",
        ["Default", "Marks (High to Low)", "Marks (Low to High)", "Deadline (Nearest first)",
         "Deadline (Furthest first)"],
        index=0
    )

    # Function to sort projects
    def sort_projects(projects, sort_option):
        projects_list = list(projects.items())

        if sort_option == "Marks (High to Low)":
            projects_list.sort(key=lambda x: x[1]['marks'], reverse=True)
        elif sort_option == "Marks (Low to High)":
            projects_list.sort(key=lambda x: x[1]['marks'])
        elif sort_option == "Deadline (Nearest first)":
            projects_list.sort(key=lambda x: x[1]['deadline'])
        elif sort_option == "Deadline (Furthest first)":
            projects_list.sort(key=lambda x: x[1]['deadline'], reverse=True)

        return projects_list
    
    # Display Projects
    st.header("Your Projects")
    st.caption(f"Currently sorted by: **{sort_option}**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("In Progress")
        if not st.session_state.in_progress:
            st.info("No projects in progress")
        else:
            sorted_projects = sort_projects(st.session_state.in_progress, sort_option)
            for project_id, project in sorted_projects:
                with st.expander(f"📝 {project['name']} - {project['subject']}"):
                    st.write(f"**Marks:** {project['marks']}")
                    st.write(f"**Deadline:** {project['deadline']}")
                    st.write(f"**Description:** {project['description']}")
                    if st.button(f"✅ Mark as Completed", key=f"complete_{project_id}"):
                        st.session_state.completed[project_id] = project
                        st.session_state.completed[project_id]['status'] = "Completed"
                        del st.session_state.in_progress[project_id]
                        st.rerun()
                    if st.button(f"✏️ Edit", key=f"edit_{project_id}"):
                        st.session_state.editing_project_key = project_id
                        st.session_state.show_project_form = True
                        st.rerun()
    
    with col2:
        st.subheader("Completed")
        if not st.session_state.completed:
            st.info("No completed projects")
        else:
            sorted_completed = sort_projects(st.session_state.completed, sort_option)
            for project_id, project in sorted_completed:
                with st.expander(f"✅ {project['name']} - {project['subject']}"):
                    st.write(f"**Marks:** {project['marks']}")
                    st.write(f"**Deadline:** {project['deadline']}")
                    st.write(f"**Description:** {project['description']}")
                    if st.button(f"🗑️ Delete", key=f"delete_{project_id}"):
                        del st.session_state.completed[project_id]
                        st.rerun()
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.email = ""
        st.session_state.show_project_form = False
        st.session_state.sort_option = "Default"
        st.rerun()

# Main app control flow
if not st.session_state.logged_in:
    login_page()
else:
    main_page()