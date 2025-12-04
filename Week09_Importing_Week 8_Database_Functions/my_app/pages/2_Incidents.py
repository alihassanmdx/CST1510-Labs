import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident

st.set_page_config(page_title="Incidents", page_icon="⚠️", layout="wide")

def get_conn():
    return connect_database()

conn = get_conn()

if not st.session_state.get("logged_in", False):
    st.error("You must log in first.")
    st.stop()

st.title("⚠️ Cybersecurity Incidents")

# Add new incident
with st.form("add_incident"):
    title = st.text_input("Title")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    submitted = st.form_submit_button("Save")

    if submitted and title:
        insert_incident(
            conn,
            date=pd.Timestamp.today().strftime("%Y-%m-%d"),
            incident_type=title,
            severity=severity,
            status=status,
            description="N/A",
            reported_by=st.session_state.get("username")
        )
        st.success("Incident added.")

# View incidents
inc = get_all_incidents(conn)
df = pd.DataFrame(inc)
st.dataframe(df)

# Update/delete
if inc is not None and len(inc) > 0:
    selected_id = st.selectbox("Select Incident ID", df["id"])

    new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])
    if st.button("Update Status"):
        update_incident_status(conn, selected_id, new_status)
        st.success("Updated.")

    if st.button("Delete Incident"):
        delete_incident(conn, selected_id)
        st.success("Deleted.")
