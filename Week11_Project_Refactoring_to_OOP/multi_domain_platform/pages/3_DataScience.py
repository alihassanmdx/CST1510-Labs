import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from models.dataset import Dataset

st.set_page_config(page_title="Data Science", layout="wide")

db = DatabaseManager("database/intelligence_platform.db")
db.connect()
auth = AuthManager(db)

api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found in secrets. Please add it to .streamlit/secrets.toml")
    st.stop()

ai = AIAssistant(api_key=api_key, system_prompt="You are a data science expert.")

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

st.title("Data Science")
st.subheader("Metrics and dataset analysis")

tab1, tab2 = st.tabs(["Model Performance", "AI Assistance"])

with tab1:
    st.write("### Model Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy", "94.2%")
    col2.metric("Precision", "91.8%")
    col3.metric("Recall", "89.5%")
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
    # Fetch datasets from DB using DatabaseManager
    dataset_rows = db.fetch_all(
        "SELECT id, dataset_name, file_size_mb, record_count, source FROM datasets_metadata"
    )
    datasets: list[Dataset] = [
        Dataset(
            dataset_id=row[0],
            name=row[1],
            size_bytes=int(row[2] * 1024 * 1024) if row[2] else 0,  # Convert MB to bytes
            rows=row[3],
            source=row[4]
        ) for row in dataset_rows
    ]

    if datasets:
        data_dist = pd.DataFrame({
            "Dataset": [d.get_name() for d in datasets],
            "Rows": [d.get_rows() for d in datasets],
        })
        st.bar_chart(data_dist, x="Dataset", y="Rows")
    else:
        st.info("No datasets found in the system.")
    st.divider()

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

with tab2:
    st.subheader("AI Assistance")

    if datasets:
        dataset_options = [
            f"{d.get_id()}: {d.get_name()} ({d.get_rows()} rows)" for d in datasets
        ]
        selected_idx = st.selectbox(
            "Select dataset to analyze:",
            range(len(datasets)),
            format_func=lambda i: dataset_options[i]
        )

        dataset = datasets[selected_idx]

        st.subheader("Dataset Details")
        st.write(f"**Name:** {dataset.get_name()}")
        st.write(f"**Rows:** {dataset.get_rows()}")
        st.write(f"**Size (MB):** {dataset.calculate_size_mb():.2f}")
        st.write(f"**Source:** {dataset.get_source()}")

        if st.button("Analyze with AI", type="primary"):
            with st.spinner("AI analyzing dataset..."):
                prompt = f"""Analyze this dataset:

Name: {dataset.get_name()}
Rows: {dataset.get_rows()}
Size (MB): {dataset.calculate_size_mb():.2f}
Source: {dataset.get_source()}

Provide:
1. Data quality assessment
2. Suggestions for preprocessing
3. Recommended visualization techniques
4. Potential insights"""
                ai_result = ai.send_message(prompt)
                st.subheader("AI Analysis")
                st.write(ai_result)
    else:
        st.info("No datasets available for analysis.")