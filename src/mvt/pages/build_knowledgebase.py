import os
import streamlit as st
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.roles not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Build Knowledge Base")

if st.button("Update Knowledge Base"):
  os.system('python ingest_test.py')
  st.write("Done!")