from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from menu import menu_with_redirect
from data_engine import get_sql_query, run_sql_query, load_analytics
import re

config_data = load_yaml_file("config.yaml")
load_dotenv(find_dotenv())

def show_charts(sql_query, granularity, start_date, end_date):
    # Replace placeholders, apply date filters and display results
    if granularity:
        sql_query = sql_query.replace("{granularity}", granularity)

    # Build WHERE clause dynamically
    where_clauses = []
    
    if start_date:
        where_clauses.append(f"period >= '{start_date}'")

    if end_date:
        where_clauses.append(f"period <= '{end_date}'")

    if where_clauses:
        sql_query = re.sub(
            r"FROM\s+(\w+)", # Get the table name
            lambda m: f"{m.group(0)} WHERE {' AND '.join(where_clauses)}",
            sql_query,
            count=1
        )
    
    # Run query
    df = run_sql_query(sql_query)

    if not df.empty:
        st.write("### Results")
        st.dataframe(df)

        # Display chart if numeric column exists
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if numeric_cols:
            x_col = df.columns[0]
            y_col = numeric_cols[0]
            st.write("### Chart")
            st.bar_chart(df, x=x_col, y=y_col)
        else:
            st.warning("No numeric columns found for chart.")
    else:
        st.warning("No data returned.")

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()
st.title("AIFAQ Analytics Dashboard")

# Free-text input
question = st.text_input("Ask a question about your chatbot data:")

# Load predefined queries
analytics_options = load_analytics()

if analytics_options:
    query_titles = [opt["title"] for opt in analytics_options]
    selected_title = st.selectbox(
        "Select an analytics query:",
        options=query_titles,
        index=None,
        placeholder="No selection",
    )

    # Get full query object
    selected_query = next((opt for opt in analytics_options if opt["title"] == selected_title), None)
else:
    selected_query = None

# Process selected query
if selected_query:
    sql_template = selected_query["sql_query"]

    # Granularity widget (only if query contains placeholder and supports options)
    if "{granularity}" in sql_template and selected_query.get("options"):
        granularity = st.radio(
            "Select granularity:",
            options=selected_query["options"],
            horizontal=True,
            index=0
        )
        sql_query = sql_template.replace("{granularity}", granularity)
    else:
        sql_query = sql_template

    # Two columns to display date inputs horizontally
    col1, col2 = st.columns(2)

    # Optional date filters
    start_date = col1.date_input("Start date:", value=None)
    end_date = col2.date_input("End date:", value=None)

    if st.button("Run query"):
        show_charts(sql_query, granularity, start_date=start_date, end_date=end_date)

# Process free-text query
elif question:
    sql_query = get_sql_query(question)
    if sql_query:
        show_charts(sql_query, None, None, None)
else:
    st.warning("Select a query or ask a question to see results.")