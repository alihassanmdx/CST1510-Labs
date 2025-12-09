import streamlit as st
import pandas as pd
from openai import OpenAI
from app.data.db import connect_database

st.set_page_config(page_title="IT Operations", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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

st.title("IT Operations")
st.subheader("System monitoring and infrastructure management")

tab1, tab2 = st.tabs(["System Monitoring", "AI Operations"])

with tab1:
    st.write("### System Health")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "CPU Usage",
            "67%",
        )

    with col2:
        st.metric(
            "Memory",
            "8.2 GB",
        )

    with col3:
        st.metric(
            "Uptime",
            "99.8%",
        )

    st.divider()

    st.write("### Resource Usage Over Time")
    usage = pd.DataFrame({
        "time": ["00:00", "06:00", "12:00", "18:00", "23:59"],
        "CPU": [45, 52, 78, 82, 67],
        "Memory": [6.2, 6.8, 8.5, 9.1, 8.2]
    })

    st.line_chart(usage, x="time", y=["CPU", "Memory"])
    st.divider()

    st.write("### Network Traffic")

    network = pd.DataFrame({
        "hour": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "23:59"],
        "incoming": [120, 90, 250, 380, 420, 340, 180],
        "outgoing": [80, 60, 180, 280, 320, 260, 140]
    })

    st.area_chart(network, x="hour", y=["incoming", "outgoing"])
    st.divider()

    st.write("### Service Status")
    col1, col2 = st.columns(2)

    with col1:
        st.success("Web Server - Running")
        st.success("Database - Running")
        st.success("API Gateway - Running")

    with col2:
        st.warning("Email Service - Degraded")
        st.success("Cache Server - Running")
        st.error("Backup Service - Down")
    st.divider()

    st.write("### Storage Usage")
    storage = pd.DataFrame({
        "server": ["Server 1", "Server 2", "Server 3", "Server 4"],
        "usage_gb": [450, 680, 320, 590]
    })

    st.bar_chart(storage, x="server", y="usage_gb")
    st.divider()

with tab2:
    st.subheader("AI Analyzer")
    system_issues = [
        {
            "id": 1,
            "issue_type": "High CPU Usage",
            "severity": "High",
            "description": "Server CPU usage at 82% for past 4 hours",
            "status": "Open",
            "affected_system": "Web Server"
        },
        {
            "id": 2,
            "issue_type": "Service Down",
            "severity": "Critical",
            "description": "Backup Service failed to start after maintenance",
            "status": "Open",
            "affected_system": "Backup Server"
        },
        {
            "id": 3,
            "issue_type": "Memory Warning",
            "severity": "Medium",
            "description": "Memory usage at 8.2 GB, approaching capacity",
            "status": "Investigating",
            "affected_system": "Database Server"
        },
        {
            "id": 4,
            "issue_type": "Network Latency",
            "severity": "Medium",
            "description": "Increased network latency during peak hours",
            "status": "Open",
            "affected_system": "Network Infrastructure"
        }
    ]

    if system_issues:
        issue_options = [
            f"{issue['id']}: {issue['issue_type']} - {issue['severity']}"
            for issue in system_issues
        ]

        selected_idx = st.selectbox(
            "Select system issue to analyze:",
            range(len(system_issues)),
            format_func=lambda i: issue_options[i]
        )

        issue = system_issues[selected_idx]
        st.subheader("Issue Details")
        st.write(f"**Type:** {issue['issue_type']}")
        st.write(f"**Severity:** {issue['severity']}")
        st.write(f"**Description:** {issue['description']}")
        st.write(f"**Status:** {issue['status']}")
        st.write(f"**Affected System:** {issue['affected_system']}")

        if st.button("Analyze with AI assistance", type="primary"):
            with st.spinner("AI analyzing system issue..."):
                analysis_prompt = f"""Analyze this IT operations issue:

Type: {issue['issue_type']}
Severity: {issue['severity']}
Description: {issue['description']}
Status: {issue['status']}
Affected System: {issue['affected_system']}

Provide:
1. Root cause analysis
2. Immediate troubleshooting steps
3. Long-term optimization recommendations
4. Impact assessment"""
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an IT operations expert."
                        },
                        {
                            "role": "user",
                            "content": analysis_prompt
                        }
                    ]
                )
                st.subheader("AI Analysis")
                st.write(response.choices[0].message.content)
conn.close()