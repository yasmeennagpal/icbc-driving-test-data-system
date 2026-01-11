import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICBC Driving Test Dashboard", layout="wide")

st.title("🚗 ICBC Driving Test Performance Dashboard")

@st.cache_data
def load_data():
    return pd.DataFrame({
        "Year": [2021, 2022, 2023, 2023, 2022, 2021],
        "Test Type": ["Class 5", "Class 5", "Class 5", "Class 7", "Class 7", "Class 7"],
        "Pass Rate (%)": [58, 61, 64, 45, 47, 49],
        "Attempts": [120000, 130000, 140000, 90000, 95000, 98000]
    })

df = load_data()

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year(s)",
    options=df["Year"].unique(),
    default=list(df["Year"].unique())
)

test_type = st.sidebar.multiselect(
    "Select Test Type",
    options=df["Test Type"].unique(),
    default=list(df["Test Type"].unique())
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["Test Type"].isin(test_type))
]

col1, col2, col3 = st.columns(3)

col1.metric("Average Pass Rate (%)", f"{filtered_df['Pass Rate (%)'].mean():.1f}")
col2.metric("Total Attempts", f"{filtered_df['Attempts'].sum():,}")
col3.metric("Number of Records", len(filtered_df))

st.divider()

st.subheader("Pass Rate Trends")
st.line_chart(
    filtered_df.pivot_table(
        index="Year",
        columns="Test Type",
        values="Pass Rate (%)"
    )
)

st.subheader("Raw Data")
st.dataframe(filtered_df, use_container_width=True)
