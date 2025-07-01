import streamlit as st
from menu import menu_with_redirect
import csv
import os

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# User Feedback (Admin)")
st.markdown("View all user feedback submitted through the app.")

feedback_file = os.path.join(os.path.dirname(__file__), '../../feedback.csv')
feedback_file = os.path.abspath(feedback_file)

feedback_data = []
if os.path.isfile(feedback_file):
    with open(feedback_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        feedback_data = list(reader)
else:
    st.info("No feedback has been submitted yet.")

if feedback_data:
    # Search box
    search_term = st.text_input("Search feedback:", "")
    if search_term:
        filtered = [row for row in feedback_data if search_term.lower() in row['feedback'].lower() or search_term.lower() in row['username'].lower()]
    else:
        filtered = feedback_data

    st.markdown(f"**Total feedback entries:** {len(filtered)}")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # Download button
    st.download_button(
        label="Download as CSV",
        data=open(feedback_file, 'rb').read(),
        file_name="feedback.csv",
        mime="text/csv"
    ) 