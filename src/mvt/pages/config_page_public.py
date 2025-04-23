from utils import load_yaml_file
import streamlit as st
from menu import menu_with_redirect
from base_config_page import save_config

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Config Page Public Dataset")

# Read config data
config_data = load_yaml_file("config.yaml")

dataset_public_path = config_data["dataset_public_path"]

save_config(dataset_public_path)