import streamlit as st
import uuid
from datetime import date, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------------
# Users dictionary
# -------------------------------
users = {
    "Waleed": {
        "password": "1234",
        "email": ""
    },
    "Abdullah": {
        "password": "12345",
        "email": ""
    },
    "Shaden": {
        "password": "123456",
        "email": ""
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

            if days_left <2 :
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

send_reminder_emails()

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

# Login Page
if not st.session_state.logged_in:
    st.title("🔐 Trackify")
    st.badge("Your project Tracker 🤩!", color="orange")
    username = st.text_input("Username")
    email = st.text_input("Your Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            if "@" not in email or "." not in email.split("@")[-1]:
                st.error("❌ Please enter a valid email address")
            else:
                # Update the email in the users dictionary
                users[username]["email"] = email
                
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.email = email

                if "projects" in users[username]:
                    for project_id, project in users[username]["projects"].items():
                        uid = str(uuid.uuid4())
                        st.session_state.in_progress[uid] = project


                if username not in st.session_state.user_data:
                    st.session_state.user_data[username] = []
                st.success(f"Welcome, {username}!")
                st.rerun()
        else:
            st.error("❌ Invalid username or password")

# Main App Page
if st.session_state.logged_in:
    st.title(f"Welcome to Trackify, {st.session_state.username}!")
    
    # Add Project Button
    if st.button("➕ Add New Project"):
        st.session_state.show_project_form = True
    
    # Project Form (appears as popup when button is clicked)
    if st.session_state.show_project_form:
        with st.form("add_project_form"):
            st.subheader("Add New Project")
            project_name = st.text_input("Project Name*", key="project_name")
            subject = st.text_input("Subject", key="subject")
            marks = st.number_input("Marks", min_value=0, max_value=100, key="marks")
            deadline = st.date_input("Deadline", key="deadline")
            description = st.text_area("Description", key="description")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Submit"):
                    if not project_name:
                        st.error("Project name is required!")
                    else:
                        project_id = str(uuid.uuid4())
                        st.session_state.in_progress[project_id] = {
                            "name": project_name,
                            "subject": subject,
                            "marks": marks,
                            "deadline": deadline,
                            "description": description,
                            "status": "In Progress"
                        }
                        st.session_state.show_project_form = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_project_form = False
                    st.rerun()
    
    # Display Projects
    st.header("Your Projects")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("In Progress")
        if not st.session_state.in_progress:
            st.info("No projects in progress")
        else:
            for project_id, project in st.session_state.in_progress.items():
                with st.expander(f"📝 {project['name']} - {project['subject']}"):
                    st.write(f"**Marks:** {project['marks']}")
                    st.write(f"**Deadline:** {project['deadline']}")
                    st.write(f"**Description:** {project['description']}")
                    if st.button(f"✅ Mark as Completed", key=f"complete_{project_id}"):
                        st.session_state.completed[project_id] = project
                        st.session_state.completed[project_id]['status'] = "Completed"
                        del st.session_state.in_progress[project_id]
                        st.rerun()
    
    with col2:
        st.subheader("Completed")
        if not st.session_state.completed:
            st.info("No completed projects")
        else:
            for project_id, project in st.session_state.completed.items():
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
        st.rerun()