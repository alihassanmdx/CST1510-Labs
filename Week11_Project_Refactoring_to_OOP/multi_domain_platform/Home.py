import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from models.user import User

st.set_page_config(page_title="Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

db = DatabaseManager("database/intelligence_platform.db")
db.connect()
auth = AuthManager(db)

current_user: User | None = st.session_state.get("current_user")
if st.session_state.logged_in and current_user is not None:
    st.success(
        f"Logged in as {current_user.get_username()} ({current_user.get_role()})"
    )
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        user: User | None = auth.login_user(username, password)
        if user is None:
            st.error("Invalid username or password")
        else:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.session_state.current_role = user.get_role()
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")

with tab2:
    st.subheader("Register")
    new_username = st.text_input("Username", key="reg_user")
    new_password = st.text_input("Password", type="password", key="reg_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):
        if not new_username or not new_password:
            st.warning("Fill all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            try:
                auth.register_user(new_username, new_password, role="user")
                st.success("Account created! Go to Login tab")
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.rerun()