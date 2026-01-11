import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICBC Driving Test Dashboard", layout="wide")

st.title("🚗 ICBC Driving Test Performance Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("data/driving_tests_clean.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

locations = st.sidebar.multiselect(
    "Select Location(s)",
    options=df["Location"].unique(),
    default=list(df["Location"].unique())
)

result_filter = st.sidebar.multiselect(
    "Result",
    options=df["Result"].unique(),
    default=list(df["Result"].unique())
)

filtered_df = df[
    (df["Location"].isin(locations)) &
    (df["Result"].isin(result_filter))
]

# Metrics
col1, col2, col3 = st.columns(3)

pass_rate = (filtered_df["PassFlag"].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
col1.metric("Pass Rate", f"{pass_rate:.1f}%")
col2.metric("Total Tests", len(filtered_df))
col3.metric("Average Errors", f"{filtered_df['Errors'].mean():.2f}")

st.divider()

# Pass rate by location
st.subheader("📍 Pass Rate by Location")
pass_by_location = filtered_df.groupby("Location")["PassFlag"].mean() * 100
st.bar_chart(pass_by_location)

# Raw data
st.subheader("📋 Test Details")
st.dataframe(filtered_df, use_container_width=True)