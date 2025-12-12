import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

st.set_page_config(page_title="Dashboard", layout="wide")

db = DatabaseManager('database/intelligence_platform.db')
db.connect()
auth = AuthManager(db)

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
st.title("Main Dashboard")

incident_rows = db.fetch_all(
    "SELECT id, incident_type, severity, status, description FROM cyber_incidents"
)
incidents: list[SecurityIncident] = []
for row in incident_rows:
    inc = SecurityIncident(
        incident_id=row[0],
        incident_type=row[1],
        severity=row[2],
        status=row[3],
        description=row[4],
    )
    incidents.append(inc)

dataset_rows = db.fetch_all(
    "SELECT id, dataset_name, file_size_mb, record_count, source FROM datasets_metadata"
)
datasets: list[Dataset] = []
for row in dataset_rows:
    ds = Dataset(
        dataset_id=row[0],
        name=row[1],
        size_bytes=int(row[2] * 1024 * 1024) if row[2] else 0,
        rows=row[3],
        source=row[4],
    )
    datasets.append(ds)

ticket_rows = db.fetch_all(
    "SELECT id, subject, priority, status, assigned_to FROM it_tickets"
)
tickets: list[ITTicket] = []
for row in ticket_rows:
    t = ITTicket(
        ticket_id=row[0],
        title=row[1],
        priority=row[2],
        status=row[3],
        assigned_to=row[4],
    )
    tickets.append(t)

df_incidents = pd.DataFrame([{
    "Type": i.get_incident_type(),
    "Severity": i.get_severity(),
    "Status": i.get_status(),
    "Description": i.get_description()
} for i in incidents]) if incidents else pd.DataFrame()

df_datasets = pd.DataFrame([{
    "Name": d.get_name(),
    "Size (MB)": d.calculate_size_mb(),
    "Rows": d.get_rows(),
    "Source": d.get_source()
} for d in datasets]) if datasets else pd.DataFrame()

df_tickets = pd.DataFrame([{
    "ID": t.get_id(),
    "Title": t.get_title(),
    "Priority": t.get_priority(),
    "Status": t.get_status(),
    "Assigned To": t.get_assigned_to() or "Unassigned"
} for t in tickets]) if tickets else pd.DataFrame()


col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(df_incidents))
col2.metric("Datasets Available", len(df_datasets))
col3.metric(
    "Open Tickets",
    len(df_tickets[df_tickets["Status"] == "Open"]) if not df_tickets.empty else 0
)

st.divider()
st.subheader("Quick View")

st.write("### Security Incidents")
if not df_incidents.empty:
    st.dataframe(df_incidents, use_container_width=True)
else:
    st.info("No incidents found")

st.write("### Datasets")
if not df_datasets.empty:
    st.dataframe(df_datasets, use_container_width=True)
else:
    st.info("No datasets found")

st.write("### IT Tickets")
if not df_tickets.empty:
    st.dataframe(df_tickets, use_container_width=True)
else:
    st.info("No tickets found")