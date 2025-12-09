import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents

st.set_page_config(page_title="Cybersecurity", layout="wide")

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

st.title("Cybersecurity")
st.subheader("Security metrics and threat monitoring")

st.write("### Security Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Threats Detected", 247, delta="+12")

with col2:
    st.metric("Vulnerabilities", 8, delta="-3")

with col3:
    st.metric("Incidents", 3, delta="+1")
st.divider()

st.write("### Threat Distribution")
threat_data = pd.DataFrame({
    "threat_type": ["Malware", "Phishing", "DDoS", "Intrusion"],
    "count": [89, 67, 45, 46]
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
col1, col2 = st.columns(2)

with col1:
    st.success("Firewall - Active")
    st.success("Antivirus - Updated")
    st.success("IDS/IPS - Running")

with col2:
    st.warning("Patch Management - 3 Pending")
    st.success("Encryption - Enabled")
    st.error("VPN Gateway - Issue Detected")
st.divider()

st.write("### Recent Security Incidents")
incidents = get_all_incidents(conn)
df = pd.DataFrame(incidents)

if len(df) > 0:
    recent = df.head(5)[['date', 'incident_type', 'severity', 'status']]
    st.dataframe(recent, use_container_width=True)
else:
    st.info("No recent incidents.")
st.divider()
st.write("### Incidents by Severity")

if len(df) > 0:
    severity_data = df['severity'].value_counts()
    st.bar_chart(severity_data)
else:
    st.info("No data available.")
st.divider()
