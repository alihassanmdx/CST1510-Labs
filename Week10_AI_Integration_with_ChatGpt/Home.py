import streamlit as st
import bcrypt
from app.data.db import connect_database
from app.data.users import verify_user, get_user_role, insert_user, get_user_by_username

st.set_page_config(page_title="Login")
def get_conn():
    return connect_database()
conn = get_conn()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

st.title("Login Page")
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.username}")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab1, tab2 = st.tabs(["Login", "Register"])
with tab1:
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = get_user_role(username)
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

with tab2:
    st.subheader("Register")
    new_user = st.text_input("Username", key="reg_user")
    new_pass = st.text_input("Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):
        if not new_user or not new_pass:
            st.warning("Fill all fields")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match")
        elif get_user_by_username(new_user):
            st.error("Username exists")
        else:
            hashed_pw = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
            insert_user(new_user, hashed_pw)
            st.success("Account created! Go to Login tab")