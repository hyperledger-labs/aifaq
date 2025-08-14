from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from menu import menu_with_redirect
from data_engine import get_sql_query, run_sql_query, load_analytics, get_analytics_query

def show_charts(sql_query):
    # Run SQL query and get DataFrame
    df = run_sql_query(sql_query)
    if not df.empty:
        # Display DataFrame as table
        st.write("### Results")
        st.dataframe(df)
        # Display as bar chart (auto-detect numeric columns)
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if numeric_cols:
            x_col = df.columns[0]  # Use first column as x-axis
            y_col = numeric_cols[0]  # Use first numeric column as y-axis
            st.write("### Chart")
            st.bar_chart(df, x=x_col, y=y_col)
        else:
            st.warning("No numeric columns found for chart.")
    else:
        st.warning("No data returned.")

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()
config_data = load_yaml_file("config.yaml")
load_dotenv(find_dotenv())

st.title("AIFAQ Analytics Dashboard")

# User input
question = st.text_input("Ask a question about your chatbot data:")

options = load_analytics()
if options:
    values = [option["value"] for option in options]
    value_to_key = {option["value"]: option["key"] for option in options}
    # select box with no intial selection
    selected_value = st.selectbox(
        "Select an analytics query:",
        options=values,
        index=None,
        placeholder="No selection",
    )

# Only process one query at a time
if selected_value:
    selected_key = value_to_key[selected_value]
    sql_query = get_analytics_query(selected_key)
    if sql_query:
        show_charts(sql_query)
elif question:
    sql_query = get_sql_query(question)
    if sql_query:
        show_charts(sql_query)
else:
    st.warning("Select a query or ask a question to see results.")
