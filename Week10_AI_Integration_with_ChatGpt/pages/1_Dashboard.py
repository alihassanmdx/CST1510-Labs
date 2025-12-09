import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

st.set_page_config(page_title="Dashboard", layout="wide")
def get_conn():
    return connect_database()

conn = get_conn()

if not st.session_state.get("logged_in", False):
    st.error("You must log in first.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.switch_page("Home.py")

st.title("Main Dashboard")

incidents = get_all_incidents(conn)
datasets = get_all_datasets(conn)
tickets = get_all_tickets(conn)

col1, col2, col3 = st.columns(3)

col1.metric("Total Incidents", len(incidents))
col2.metric("Datasets Available", len(datasets))
col3.metric("Open Tickets", len(tickets[tickets["status"] == "Open"]))

st.divider()
st.subheader("Quick View")
st.write("### Cyber Incidents")
st.dataframe(pd.DataFrame(incidents), use_container_width=True)

st.write("### Datasets Metadata")
st.dataframe(pd.DataFrame(datasets), use_container_width=True)

st.write("### Tickets")
st.dataframe(pd.DataFrame(tickets), use_container_width=True)