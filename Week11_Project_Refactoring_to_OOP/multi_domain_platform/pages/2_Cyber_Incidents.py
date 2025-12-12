import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from models.security_incident import SecurityIncident
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cybersecurity Incidents", layout="wide")

db = DatabaseManager("database/intelligence_platform.db")
db.connect()
auth = AuthManager(db)

api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found in secrets. Please add it to .streamlit/secrets.toml")
    st.stop()

ai = AIAssistant(api_key=api_key, system_prompt="You are a cybersecurity expert.")

current_user = st.session_state.get("current_user")
if current_user is None:
    st.error("You must log in first.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.switch_page("Home.py")

st.title("Cybersecurity Incidents")
st.subheader("Monitor and analyze security incidents")

def fetch_all_incidents():
    """Fetch all incidents and convert to SecurityIncident objects."""
    rows = db.fetch_all(
        "SELECT id, date, incident_type, severity, status, description, reported_by FROM cyber_incidents ORDER BY id DESC"
    )

    incidents: list[SecurityIncident] = []
    for row in rows:
        inc = SecurityIncident(
            incident_id=row[0],
            incident_type=row[2],
            severity=row[3],
            status=row[4],
            description=row[5],
        )
        incidents.append(inc)

    return incidents, rows


incidents, rows = fetch_all_incidents()
df = pd.DataFrame([{
    "id": row[0],
    "date": row[1],
    "incident_type": row[2],
    "severity": row[3],
    "status": row[4],
    "description": row[5]
} for row in rows]) if rows else pd.DataFrame()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["All Incidents", "Add New", "Update Status", "Delete Incident", "AI Analysis"])

with tab1:
    st.subheader("All Incidents")

    if len(incidents) > 0:
        incident_data = pd.DataFrame([{
            "ID": inc.get_id(),
            "Type": inc.get_incident_type(),
            "Severity": inc.get_severity(),
            "Severity Level": inc.get_severity_level(),
            "Status": inc.get_status(),
            "Description": inc.get_description()
        } for inc in incidents])

        st.dataframe(incident_data, use_container_width=True)
        st.divider()

        st.subheader("Security Metrics")
        col1, col2, col3 = st.columns(3)

        threats_detected = sum(1 for inc in incidents if inc.get_status() == 'Open')
        col1.metric("Threats Detected", threats_detected)

        vulnerabilities = sum(1 for inc in incidents if inc.get_severity_level() >= 3)
        col2.metric("Vulnerabilities", vulnerabilities)

        incidents_count = len(incidents)
        col3.metric("Incidents", incidents_count)

        st.divider()
        st.subheader("Threat Distribution")
        threat_data = pd.DataFrame([inc.get_incident_type() for inc in incidents], columns=["Type"])
        threat_counts = threat_data['Type'].value_counts()
        st.bar_chart(threat_counts)

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
                db.execute_query(
                    """INSERT INTO cyber_incidents 
                       (date, incident_type, severity, status, description, reported_by) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (str(incident_date), incident_type, severity, status, description, current_user.get_username())
                )
                st.success("Incident added successfully!")
                st.rerun()

with tab3:
    st.subheader("Update Incident Status")
    if len(incidents) > 0:
        incident_options = {
            inc.get_id(): f"ID {inc.get_id()}: {inc.get_incident_type()} - {inc.get_severity()}"
            for inc in incidents
        }

        selected_id = st.selectbox("Select Incident", list(incident_options.keys()),
                                   format_func=lambda x: incident_options[x])

        selected_incident = next(inc for inc in incidents if inc.get_id() == selected_id)

        st.write(f"**Current Status:** {selected_incident.get_status()}")
        st.write(f"**Type:** {selected_incident.get_incident_type()}")
        st.write(f"**Severity:** {selected_incident.get_severity()} (Level {selected_incident.get_severity_level()})")
        st.write(f"**Description:** {selected_incident.get_description()}")
        st.divider()

        with st.form("update_form"):
            new_status = st.selectbox("New Status", ["Open", "Investigating", "Closed"])
            new_severity = st.selectbox("New Severity", ["Low", "Medium", "High", "Critical"])
            update_btn = st.form_submit_button("Update Incident", type="primary")

            if update_btn:
                # Update using DatabaseManager
                db.execute_query(
                    "UPDATE cyber_incidents SET status = ?, severity = ? WHERE id = ?",
                    (new_status, new_severity, selected_id)
                )
                st.success(f"Incident {selected_id} updated successfully!")
                st.rerun()
    else:
        st.info("No incidents to update.")

with tab4:
    st.subheader("Delete Incident")
    if len(incidents) > 0:
        incident_options = {
            inc.get_id(): f"ID {inc.get_id()}: {inc.get_incident_type()}"
            for inc in incidents
        }

        selected_id = st.selectbox("Select Incident ID to Delete", list(incident_options.keys()),
                                   format_func=lambda x: incident_options[x], key="delete_select")
        selected_incident = next(inc for inc in incidents if inc.get_id() == selected_id)

        st.write(f"**Type:** {selected_incident.get_incident_type()}")
        st.write(f"**Severity:** {selected_incident.get_severity()} (Level {selected_incident.get_severity_level()})")
        st.write(f"**Status:** {selected_incident.get_status()}")
        st.write(f"**Description:** {selected_incident.get_description()}")
        st.divider()

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Delete", type="primary"):
                # Delete using DatabaseManager
                db.execute_query(
                    "DELETE FROM cyber_incidents WHERE id = ?",
                    (selected_id,)
                )
                st.success(f"Incident {selected_id} deleted!")
                st.rerun()
    else:
        st.info("No incidents to delete.")
with tab5:
    st.subheader("AI-Powered Incident Analysis")

    if len(incidents) > 0:
        incident_options = [
            f"{inc.get_id()}: {inc.get_incident_type()} [{inc.get_severity()}]"
            for inc in incidents
        ]

        selected_idx = st.selectbox(
            "Select incident to analyze:",
            range(len(incidents)),
            format_func=lambda i: incident_options[i],
            key="ai_analysis_select"
        )

        incident = incidents[selected_idx]

        st.divider()
        st.subheader("Incident Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {incident.get_id()}")
            st.write(f"**Type:** {incident.get_incident_type()}")
            st.write(f"**Severity:** {incident.get_severity()}")
            st.write(f"**Severity Level:** {incident.get_severity_level()}")
        with col2:
            st.write(f"**Status:** {incident.get_status()}")
            st.write(f"**Description:** {incident.get_description()}")

        st.divider()

        if st.button("Analyze with AI", type="primary", use_container_width=True):
            with st.spinner("AI analyzing incident..."):
                prompt = f"""Analyze this cybersecurity incident:

Incident ID: {incident.get_id()}
Type: {incident.get_incident_type()}
Severity: {incident.get_severity()} (Level {incident.get_severity_level()}/4)
Status: {incident.get_status()}
Description: {incident.get_description()}

Provide a comprehensive analysis including:
1. Root cause analysis
2. Immediate mitigation steps
3. Long-term security recommendations
4. Potential business impact assessment
5. Similar threat patterns to watch for"""
                ai_result = ai.send_message(prompt)

                st.divider()
                st.subheader("AI Analysis Results")
                st.markdown(ai_result)
                if st.button("Clear AI History", type="secondary"):
                    ai.clear_history()
                    st.success("AI conversation history cleared!")

    else:
        st.info("No incidents available for AI analysis.")