import streamlit as st
import yaml
from utils import load_yaml_file
from database import create_connection, create_prompts_table, save_prompt, get_prompt
from menu import menu_with_redirect

# This script provides a web interface for managing system and query rewriting prompts.
# It allows admin users to view, edit, and save prompts that control the AI FAQ system behavior.
# Prompts can be loaded from config defaults or saved/retrieved from the database.

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Prompt Management")
st.markdown("Manage system and query rewriting prompts for the AI FAQ system.")

# Initialize database connection and create tables if needed
conn = create_connection()
if conn:
    create_prompts_table(conn)

# This function loads default prompts from the config.yaml file.
# Returns a dictionary with system_prompt and query_rewriting_prompt keys.
def load_default_prompts():
    """Load default prompts from config.yaml"""
    try:
        config_data = load_yaml_file("config.yaml")
        return {
            "system_prompt": config_data.get("system_prompt", ""),
            "query_rewriting_prompt": config_data.get("query_rewriting_prompt", "")
        }
    except Exception as e:
        st.error(f"Error loading config file: {e}")
        return {"system_prompt": "", "query_rewriting_prompt": ""}

# This function saves both system and query rewriting prompts to the database.
# Takes system_prompt and query_rewriting_prompt as parameters and returns success status.
def save_prompts_to_db(system_prompt, query_rewriting_prompt):
    """Save prompts to database"""
    if not conn:
        st.error("Database connection failed")
        return False
    
    try:
        success1 = save_prompt(conn, "system_prompt", system_prompt)
        success2 = save_prompt(conn, "query_rewriting_prompt", query_rewriting_prompt)
        
        if success1 and success2:
            st.success("Prompts saved successfully!")
            return True
        else:
            st.error("Failed to save prompts to database")
            return False
    except Exception as e:
        st.error(f"Error saving prompts: {e}")
        return False

# This function loads prompts from the database with fallback to config defaults.
# Returns a dictionary with both prompt types, using config values if database is empty.
def load_prompts_from_db():
    """Load prompts from database, fallback to config defaults"""
    if not conn:
        return load_default_prompts()
    
    try:
        system_prompt = get_prompt(conn, "system_prompt")
        query_rewriting_prompt = get_prompt(conn, "query_rewriting_prompt")
        
        # If prompts don't exist in DB, use config defaults
        if system_prompt is None or query_rewriting_prompt is None:
            defaults = load_default_prompts()
            system_prompt = system_prompt or defaults["system_prompt"]
            query_rewriting_prompt = query_rewriting_prompt or defaults["query_rewriting_prompt"]
        
        return {
            "system_prompt": system_prompt,
            "query_rewriting_prompt": query_rewriting_prompt
        }
    except Exception as e:
        st.error(f"Error loading prompts from database: {e}")
        return load_default_prompts()

# Initialize session state for prompts if not already set
if "current_prompts" not in st.session_state:
    st.session_state.current_prompts = load_prompts_from_db()

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("System Prompt")
    st.markdown("*This prompt defines the AI assistant's role and behavior*")

with col2:
    # Load default values button for System Prompt only
    if st.button("Load Default", help="Load default System Prompt from config.yaml"):
        defaults = load_default_prompts()
        st.session_state.current_prompts["system_prompt"] = defaults["system_prompt"]
        st.rerun()

# System Prompt Text Area - main prompt that defines AI behavior
system_prompt = st.text_area(
    "System Prompt",
    value=st.session_state.current_prompts["system_prompt"],
    height=150,
    help="Define how the AI assistant should behave and respond to questions",
    label_visibility="collapsed"
)

# Create columns for Query Rewriting Prompt section
col3, col4 = st.columns([3, 1])

with col3:
    st.subheader("Query Rewriting Prompt")
    st.markdown("*This prompt helps rewrite user queries for better document retrieval*")

with col4:
    # Load default values button for Query Rewriting Prompt only
    if st.button("Load Default", help="Load default Query Rewriting Prompt from config.yaml", key="load_default_qr"):
        defaults = load_default_prompts()
        st.session_state.current_prompts["query_rewriting_prompt"] = defaults["query_rewriting_prompt"]
        st.rerun()

# Query Rewriting Prompt Text Area - prompt for improving search queries
query_rewriting_prompt = st.text_area(
    "Query Rewriting Prompt",
    value=st.session_state.current_prompts["query_rewriting_prompt"],
    height=150,
    help="Define how user queries should be rewritten for optimal search results",
    label_visibility="collapsed"
)

# Update session state when text areas change
st.session_state.current_prompts["system_prompt"] = system_prompt
st.session_state.current_prompts["query_rewriting_prompt"] = query_rewriting_prompt

# Action buttons for saving and resetting
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    # Save changes button - persists current prompts to database
    if st.button("Save Changes", type="primary"):
        save_prompts_to_db(system_prompt, query_rewriting_prompt)

with col2:
    # Reset button - reverts to last saved values in database
    if st.button("Reset to DB", help="Reset to last saved values"):
        st.session_state.current_prompts = load_prompts_from_db()
        st.success("Reset to database values!")
        st.rerun()

# Close database connection to free resources
if conn:
    conn.close()
