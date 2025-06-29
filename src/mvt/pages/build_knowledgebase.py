import os
import streamlit as st
from menu import menu_with_redirect
import subprocess

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Build Knowledge Base")

if st.button("Update Knowledge Base"):
  msg_out = os.system(f"python ingest.py {st.session_state['username']}")
  if msg_out > 0:
     st.write(f"Error nr {msg_out}!")
  else:
     st.write(f"Done! Database updated successfully.")