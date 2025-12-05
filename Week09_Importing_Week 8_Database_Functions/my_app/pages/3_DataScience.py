import streamlit as st
import pandas as pd
from app.data.db import connect_database

st.set_page_config(page_title="Data Science", layout="wide")

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

st.title("Data Science")
st.subheader("Metrics and data analysis")

# Model performance metrics
st.write("### Model Performance")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Accuracy", "94.2%")

with col2:
    st.metric("Precision", "91.8%")

with col3:
    st.metric("Recall", "89.5%")

st.divider()

st.write("### Training History")
history = pd.DataFrame({
    "epoch": [1, 2, 3, 4, 5],
    "loss": [0.45, 0.32, 0.24, 0.18, 0.15],
    "accuracy": [0.78, 0.85, 0.89, 0.92, 0.94]
})

st.line_chart(history, x="epoch", y=["loss", "accuracy"])

st.divider()

st.write("### Data Distribution")

data_dist = pd.DataFrame({
    "category": ["Training", "Validation", "Testing"],
    "samples": [7000, 2000, 1000]
})

st.bar_chart(data_dist, x="category", y="samples")

st.divider()

# Feature correlation
st.write("### Feature Correlations")

correlation_data = pd.DataFrame({
    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "y": [2, 4, 5, 7, 8, 10, 11, 13, 14, 16]
})

st.scatter_chart(correlation_data, x="x", y="y")

st.divider()

st.write("### Confusion Matrix")

col1, col2 = st.columns(2)

with col1:
    st.metric("True Positives", "450")
    st.metric("False Positives", "38")

with col2:
    st.metric("True Negatives", "485")
    st.metric("False Negatives", "27")

st.divider()
