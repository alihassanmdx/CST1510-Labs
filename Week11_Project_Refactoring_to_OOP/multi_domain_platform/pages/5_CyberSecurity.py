import streamlit as st
import pandas as pd

from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Cybersecurity", layout="wide")
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

st.title("Cybersecurity")
st.subheader("Security metrics and threat monitoring")

db = DatabaseManager("database/intelligence_platform.db")
db.connect()

all_rows = db.fetch_all(
    """
    SELECT id, incident_type, severity, status, description
    FROM cyber_incidents
    ORDER BY id DESC
    """
)

all_incidents: list[SecurityIncident] = []
for row in all_rows:
    incident = SecurityIncident(
        incident_id=row[0],
        incident_type=row[1],
        severity=row[2],
        status=row[3],
        description=row[4],
    )
    all_incidents.append(incident)

st.write("### Security Metrics")
col1, col2, col3 = st.columns(3)

threats_detected = sum(1 for inc in all_incidents if inc.get_status() == 'Open')
vulnerabilities = sum(1 for inc in all_incidents if inc.get_severity_level() >= 3)
total_incidents = len(all_incidents)

with col1: st.metric("Threats Detected", threats_detected)
with col2: st.metric("Vulnerabilities", vulnerabilities)
with col3: st.metric("Incidents", total_incidents)
st.divider()

st.write("### Threat Distribution")
if len(all_incidents) > 0:
    threat_types = [inc.get_incident_type() for inc in all_incidents]
    threat_df = pd.DataFrame(threat_types, columns=["threat_type"])
    threat_counts = threat_df['threat_type'].value_counts()
    st.bar_chart(threat_counts)
else:
    threat_data = pd.DataFrame({
        "threat_type": ["Malware", "Phishing", "DDoS", "Intrusion"],
        "count": [0, 0, 0, 0]
    })
    st.bar_chart(threat_data, x="threat_type", y="count")
st.divider()

st.write("### Threat Trends")
trends = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Malware": [45, 52, 61, 58, 73, 89],
    "Phishing": [32, 41, 38, 45, 55, 67],
    "DDoS": [28, 25, 31, 35, 42, 45]
})
st.line_chart(trends, x="month", y=["Malware", "Phishing", "DDoS"])
st.divider()

st.write("### Attack Patterns by Hour")
attack_hours = pd.DataFrame({
    "hour": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    "attacks": [15, 8, 25, 42, 38, 28]
})
st.area_chart(attack_hours, x="hour", y="attacks")
st.divider()

st.write("### Security Status")
c1, c2 = st.columns(2)

with c1:
    st.success("Firewall - Active")
    st.success("Antivirus - Updated")
    st.success("IDS/IPS - Running")

with c2:
    st.warning("Patch Management - 3 Pending")
    st.success("Encryption - Enabled")
    st.error("VPN Gateway - Issue Detected")
st.divider()

st.write("### Recent Security Incidents")

recent_incidents = all_incidents[:10] if len(all_incidents) > 10 else all_incidents

if len(recent_incidents) > 0:
    df = pd.DataFrame([
        {
            "ID": inc.get_id(),
            "Type": inc.get_incident_type(),
            "Severity": inc.get_severity(),
            "Severity Level": inc.get_severity_level(),
            "Status": inc.get_status(),
            "Description": inc.get_description()
        }
        for inc in recent_incidents
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No recent incidents.")
st.divider()

st.write("### Incidents by Severity")

if len(all_incidents) > 0:
    severity_data = [inc.get_severity() for inc in all_incidents]
    severity_df = pd.DataFrame(severity_data, columns=["Severity"])
    severity_counts = severity_df["Severity"].value_counts()
    st.bar_chart(severity_counts)
else:
    st.info("No data available.")