import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident

st.set_page_config(page_title="Cyber Incidents", layout="wide")

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

st.title("Incident Management")

tab1, tab2, tab3, tab4 = st.tabs(["View Data", "Add Incident", "Update Status", "Delete"])

incidents = get_all_incidents(conn)
df = pd.DataFrame(incidents)

with tab1:
    st.subheader("All Incidents")

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.subheader("Security Metrics")
        col1, col2, col3 = st.columns(3)

        threats_detected = len(df[df['status'] == 'Open'])
        col1.metric("Threats Detected", threats_detected)

        vulnerabilities = len(df[df['severity'] == 'High']) + len(df[df['severity'] == 'Critical'])
        col2.metric("Vulnerabilities", vulnerabilities)

        incidents_count = len(df)
        col3.metric("Incidents", incidents_count)

        st.divider()
        st.subheader("Threat Distribution")
        threat_data = df['incident_type'].value_counts()
        st.bar_chart(threat_data)

    else:
        st.info("No incidents found.")

with tab2:
    st.subheader("Add New Incident")
    with st.form("add_incident_form"):
        incident_date = st.date_input("Date", value=datetime.now())
        incident_type = st.selectbox("Incident Type", ["Malware", "DDoS", "SQL Injection", "Phishing", "Ransomware"])
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "Investigating", "Closed"])
        description = st.text_area("Description", placeholder="Enter incident description...")

        submit = st.form_submit_button("Add Incident", type="primary")
        if submit:
            if description == "":
                st.error("Please enter a description.")
            else:
                insert_incident(conn, str(incident_date), incident_type, severity, status, description)
                st.success("Incident added successfully!")
                st.rerun()

with tab3:
    st.subheader("Update Incident Status")
    if len(df) > 0:
        incident_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Incident ID", incident_ids)
        current = df[df['id'] == selected_id].iloc[0]
        st.write(f"**Current Status:** {current['status']}")
        st.write(f"**Type:** {current['incident_type']}")
        st.write(f"**Severity:** {current['severity']}")
        st.divider()

        with st.form("update_form"):
            new_status = st.selectbox("New Status", ["Open", "Investigating", "Closed"])
            new_severity = st.selectbox("New Severity", ["Low", "Medium", "High", "Critical"])
            update_btn = st.form_submit_button("Update Incident", type="primary")

            if update_btn:
                update_incident_status(conn, selected_id, new_status)
                st.success(f"Incident {selected_id} updated successfully!")
                st.rerun()
    else:
        st.info("No incidents to update.")

with tab4:
    st.subheader("Delete Incident")
    if len(df) > 0:
        incident_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Incident ID to Delete", incident_ids, key="delete_select")
        current = df[df['id'] == selected_id].iloc[0]
        st.write(f"**Date:** {current['date']}")
        st.write(f"**Type:** {current['incident_type']}")
        st.write(f"**Status:** {current['status']}")
        st.write(f"**Description:** {current['description']}")
        st.divider()

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Delete", type="primary"):
                delete_incident(conn, selected_id)
                st.success(f"Incident {selected_id} deleted!")
                st.rerun()
    else:
        st.info("No incidents to delete.")