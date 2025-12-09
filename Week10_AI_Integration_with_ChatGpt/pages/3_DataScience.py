import streamlit as st
import pandas as pd
from openai import OpenAI
from app.data.db import connect_database

st.set_page_config(page_title="Data Science", layout="wide")
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

st.title("Data Science")
st.subheader("Metrics and data analysis")

tab1, tab2 = st.tabs(["Model Performance", "AI Operations"])

with tab1:
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
    model_scenarios = [
        {
            "id": 1,
            "model_name": "Customer Churn Prediction",
            "accuracy": "94.2%",
            "precision": "91.8%",
            "recall": "89.5%",
            "issue": "Low recall on minority class",
            "description": "Model shows bias towards majority class prediction"
        },
        {
            "id": 2,
            "model_name": "Sales Forecasting",
            "accuracy": "87.3%",
            "precision": "88.1%",
            "recall": "86.5%",
            "issue": "High error on seasonal data",
            "description": "Model struggles with holiday season predictions"
        },
        {
            "id": 3,
            "model_name": "Image Classification",
            "accuracy": "96.8%",
            "precision": "95.9%",
            "recall": "97.2%",
            "issue": "Overfitting on training data",
            "description": "Large gap between training and validation performance"
        },
        {
            "id": 4,
            "model_name": "Sentiment Analysis",
            "accuracy": "91.5%",
            "precision": "90.2%",
            "recall": "92.1%",
            "issue": "Poor handling of sarcasm",
            "description": "Model misclassifies sarcastic comments"
        }
    ]
    if model_scenarios:
        scenario_options = [
            f"{scenario['id']}: {scenario['model_name']} - {scenario['issue']}"
            for scenario in model_scenarios
        ]

        selected_idx = st.selectbox(
            "Select model to analyze:",
            range(len(model_scenarios)),
            format_func=lambda i: scenario_options[i]
        )
        scenario = model_scenarios[selected_idx]
        st.subheader("Model Details")
        st.write(f"**Model:** {scenario['model_name']}")
        st.write(f"**Accuracy:** {scenario['accuracy']}")
        st.write(f"**Precision:** {scenario['precision']}")
        st.write(f"**Recall:** {scenario['recall']}")
        st.write(f"**Issue:** {scenario['issue']}")
        st.write(f"**Description:** {scenario['description']}")

        # Analyze with AI
        if st.button("Analyze with AI assistance Chat", type="primary"):
            with st.spinner("AI analyzing model performance..."):
                # Create analysis prompt
                analysis_prompt = f"""Analyze this machine learning model:

Model Name: {scenario['model_name']}
Accuracy: {scenario['accuracy']}
Precision: {scenario['precision']}
Recall: {scenario['recall']}
Issue: {scenario['issue']}
Description: {scenario['description']}

Provide:
1. Performance assessment
2. Root cause of the issue
3. Recommended improvements
4. Data quality suggestions"""
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a data science expert."
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