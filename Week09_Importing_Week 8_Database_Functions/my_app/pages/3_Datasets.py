import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.datasets import get_all_datasets, insert_dataset

st.set_page_config(page_title="Datasets", page_icon="📚", layout="wide")

def get_conn():
    return connect_database()

conn = get_conn()

if not st.session_state.get("logged_in", False):
    st.error("Login required.")
    st.stop()

st.title("📚 Datasets Manager")

with st.form("add_dataset"):
    name = st.text_input("Dataset Name")
    source = st.text_input("Source")
    category = st.text_input("Category")
    size = st.number_input("Size (MB)", min_value=0)

    if st.form_submit_button("Add Dataset"):
        insert_dataset(conn, name, category, source, None, None, size)
        st.success("Dataset added.")

df = pd.DataFrame(get_all_datasets(conn))
st.dataframe(df)
