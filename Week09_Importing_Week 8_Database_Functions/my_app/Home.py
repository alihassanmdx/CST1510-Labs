import streamlit as st
from app.data.db import connect_database
from app.data.users import verify_user, get_user_role, insert_user, get_user_by_username

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Cache DB connection
def get_conn():
    return connect_database()

conn = get_conn()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

st.title("🔐 User Login")

# Already logged in? → Dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}** ({st.session_state.role})")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab_login, tab_register = st.tabs(["Login", "Register"])

# LOGIN
with tab_login:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In", type="primary"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = get_user_role(username)
                st.success("Login successful!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password")

# REGISTER
# REGISTER
with tab_register:
    st.subheader("Register")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not new_user or not new_pass:
            st.warning("All fields required.")

        elif new_pass != confirm:
            st.error("Passwords do not match.")

        elif get_user_by_username(new_user):
            st.error("Username already exists.")

        else:
            # Hash password with bcrypt
            import bcrypt
            hashed_pw = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())

            insert_user(new_user, hashed_pw)

            st.success("Account created! Please log in.")
            st.info("Go to the Login tab.")
