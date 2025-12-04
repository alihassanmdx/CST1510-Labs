import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.tickets import get_all_tickets, insert_ticket

st.set_page_config(page_title="Tickets", page_icon="🎫", layout="wide")
def get_conn():
    return connect_database()

conn = get_conn()

if not st.session_state.get("logged_in", False):
    st.error("Login required.")
    st.stop()

st.title("🎫 IT Tickets")

with st.form("new_ticket"):
    title = st.text_input("Title")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "Resolved"])
    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        insert_ticket(
            conn,
            ticket_id=str(pd.Timestamp.now().timestamp()),
            subject=title,
            priority=priority,
            status=status,
            category=None,
            description=None,
            created_date=pd.Timestamp.now().strftime("%Y-%m-%d"),
            assigned_to=None
        )
        st.success("Ticket Created")

df = pd.DataFrame(get_all_tickets(conn))
st.dataframe(df)
