import streamlit as st
from menu import menu_with_redirect
import csv
from datetime import datetime
import os

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.markdown("# Feedback")
st.markdown("We value your feedback! Please let us know your thoughts, suggestions, or issues below.")

# Get username if available
username = getattr(st.session_state, 'username', 'anonymous')

# Feedback form
with st.form("feedback_form"):
    feedback_text = st.text_area("Your Feedback", max_chars=1000, height=150)
    rating = st.selectbox("How would you rate your experience?", ["5 - Excellent", "4 - Good", "3 - Average", "2 - Poor", "1 - Very Poor"], index=0)
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    if not feedback_text.strip():
        st.warning("Please enter your feedback before submitting.")
    else:
        feedback_file = os.path.join(os.path.dirname(__file__), '../../feedback.csv')
        feedback_file = os.path.abspath(feedback_file)
        file_exists = os.path.isfile(feedback_file)
        with open(feedback_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "username", "rating", "feedback"])
            writer.writerow([
                datetime.now().isoformat(timespec='seconds'),
                username,
                rating.split(" - ")[0],
                feedback_text.replace('\n', ' ')
            ])
        st.success("Thank you for your feedback!")
        st.balloons() 