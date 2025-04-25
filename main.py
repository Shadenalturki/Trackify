import streamlit as st
from datetime import date
import uuid

users = {
    "Waleed": {"password": "1234", "email": ""},
    "Abdullah": {"password": "12345", "email": "3abdullah.cx@gmail.com"},
    "Shaden": {"password": "123456", "email": ""},
    "Hussah": {"password": "1234567", "email": ""}
}

## Start session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "email" not in st.session_state:
    st.session_state.email = ""

# Login Page
if not st.session_state.logged_in:
    st.title("🔐 Trackify")
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
                if username not in st.session_state.user_data:
                    st.session_state.user_data[username] = []
                st.success(f"Welcome, {username}!")
                st.rerun()
        else:
            st.error("❌ Invalid username or password")

# Main App Page
if st.session_state.logged_in:
    st.title(f"Welcome to Trackify, {st.session_state.username}!")
    
    
    
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.email = ""
        st.rerun()
    
    