import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from models.it_ticket import ITTicket

st.set_page_config(page_title="IT Operations", layout="wide")
db = DatabaseManager("database/intelligence_platform.db")
db.connect()
auth = AuthManager(db)

api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found in secrets. Please add it to .streamlit/secrets.toml")
    st.stop()

ai = AIAssistant(api_key=api_key, system_prompt="You are an IT operations expert.")

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

st.title("IT Operations")
st.subheader("System monitoring and infrastructure management")

tab1, tab2 = st.tabs(["System Monitoring", "AI Operations / Tickets"])
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
    st.subheader("AI Assistance / IT Tickets")

    # Fetch tickets from DB using DatabaseManager
    ticket_rows = db.fetch_all(
        "SELECT id, subject, priority, status, assigned_to FROM it_tickets"
    )
    tickets: list[ITTicket] = [
        ITTicket(
            ticket_id=row[0],
            title=row[1],
            priority=row[2],
            status=row[3],
            assigned_to=row[4]
        ) for row in ticket_rows
    ]

    if tickets:
        ticket_options = [f"{t.get_status()} - {t.get_title()}" for t in tickets]
        selected_idx = st.selectbox(
            "Select ticket to analyze:",
            range(len(tickets)),
            format_func=lambda i: ticket_options[i]
        )
        ticket = tickets[selected_idx]

        st.subheader("Ticket Details")
        st.write(f"**Title:** {ticket.get_title()}")
        st.write(f"**Priority:** {ticket.get_priority()}")
        st.write(f"**Status:** {ticket.get_status()}")
        st.write(f"**Assigned To:** {ticket.get_assigned_to() or 'Unassigned'}")

        if st.button("Analyze with AI", type="primary"):
            with st.spinner("AI analyzing ticket..."):
                # Build prompt using model getter methods
                prompt = f"""Analyze this IT support ticket:

Title: {ticket.get_title()}
Priority: {ticket.get_priority()}
Status: {ticket.get_status()}
Assigned To: {ticket.get_assigned_to() or 'Unassigned'}

Provide:
1. Root cause analysis
2. Immediate troubleshooting steps
3. Long-term recommendations
4. Impact assessment
"""
                ai_result = ai.send_message(prompt)
                st.subheader("AI Analysis")
                st.write(ai_result)
    else:
        st.info("No tickets found in the system.")