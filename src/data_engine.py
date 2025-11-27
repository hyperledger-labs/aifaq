import os
import pandas as pd
import streamlit as st
from mistralai import Mistral
from utils import load_yaml_file
import sqlite3

config_data = load_yaml_file("config.yaml")

def get_sql_query(question: str) -> str:
    
    prompt = config_data["analytics_prompt"] + question 

    # Get API keys
    mistral_api_key = os.getenv("MISTRALAI_API_KEY")
    model = config_data["analytics_model"]

    client = Mistral(api_key=mistral_api_key)

    response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    sql_query = response.choices[0].message.content
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query

def run_sql_query(sql_query: str) -> pd.DataFrame:
    # Run SQL query on SQLite DB and return results as DataFrame.
    conn = sqlite3.connect(config_data["dbpath"])
    try:
        df = pd.read_sql(sql_query, conn)
    except Exception as e:
        st.error(f"SQL Error: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def load_analytics():
    conn = sqlite3.connect(config_data["dbpath"])
    try:
        cursor = conn.execute("""
            SELECT
                id,
                title,
                sql_query,
                options
            FROM analytics
            ORDER BY id;
        """)
        options = []
        for row in cursor.fetchall():
            option_list = [opt.strip() for opt in row[3].split(",") if opt.strip()]
            options.append({
                "key": row[0],
                "title": row[1],
                "sql_query": row[2],
                "options": option_list
            })
    except Exception as e:
        st.error(f"Error loading analytics options: {e}")
        options = []
    finally:
        conn.close()
    return options

def get_analytics_query(query_id: int) -> str:
    conn = sqlite3.connect(config_data["dbpath"])
    try:
        cursor = conn.execute("""
            SELECT sql_query
            FROM analytics
            WHERE id = ?
        """, (query_id,))
        row = cursor.fetchone()
        sql_query = row[0] if row else None
    except Exception as e:
        st.error(f"Error fetching query: {e}")
        sql_query = None
    finally:
        conn.close()
    return sql_query
