import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Set page title
st.set_page_config(
    page_title="Employee Performance Portal",
    layout="centered"
)

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("employee_performance.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Title
st.title("📊 Employee Performance Portal")
st.write("Enter Employee ID and number of past months to get performance data")

# User Inputs
employee_id = st.text_input("Employee ID (e.g., E001)")
months = st.number_input("Number of past months", min_value=1, max_value=12, value=3)

# Button to get performance
if st.button("Get Performance"):
    if not employee_id:
        st.error("Please enter an Employee ID")
    else:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=months*30)

        result = df[(df["employee_id"] == employee_id) & (df["date"] >= start_date)]

        if result.empty:
            st.warning("No data found for this employee")
        else:
            st.success(f"Performance data for {employee_id}")
            st.dataframe(result, use_container_width=True)

            # Create Excel for download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                result.to_excel(writer, index=False, sheet_name="Performance")

            st.download_button(
                label="⬇ Download Excel",
                data=buffer.getvalue(),
                file_name=f"{employee_id}_last_{months}_months.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
