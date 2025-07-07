import streamlit as st
from database import create_connection, create_feedback_table, get_all_feedback
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# User Feedbacks")
st.markdown("View all user feedback on chatbot responses.")

conn = create_connection()
create_feedback_table(conn)
feedbacks = get_all_feedback(conn)
conn.close()

if feedbacks:
    st.markdown(f"### Overview ({len(feedbacks)} feedback entries found)")
    search_term = st.text_input("Search by username, feedback type, or reason:", placeholder="Enter search term...")
    if search_term:
        search_term_lower = search_term.lower()
        filtered_feedbacks = [
            fb for fb in feedbacks
            if search_term_lower in str(fb[1]).lower() or  # username
               search_term_lower in str(fb[3]).lower() or  # feedback_type
               (fb[5] and search_term_lower in str(fb[5]).lower())  # reason
        ]
        st.success(f"Found {len(filtered_feedbacks)} matching feedback entries")
    else:
        filtered_feedbacks = feedbacks
    st.markdown("---")
    for i, fb in enumerate(filtered_feedbacks):
        st.write(f"**{i+1}. Username:** {fb[1]}")
        st.write(f"**Message Index:** {fb[2]}")
        st.write(f"**Feedback Type:** {fb[3]}")
        st.write(f"**Response Snippet:** {fb[4]}")
        st.write(f"**Reason:** {fb[5] if fb[5] else '-'}")
        st.write(f"**Timestamp:** {fb[6]}")
        st.markdown("---")
else:
    st.info("No feedback entries found.")
