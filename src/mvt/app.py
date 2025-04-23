import streamlit as st
from menu import menu
from database import create_connection, create_table, get_user, insert_user
from homepage import gethomepage

# Get markdown homepage
st.markdown(body=gethomepage(), unsafe_allow_html=True)

# Check if user is authenticated
if not st.experimental_user.is_logged_in:
    if st.button("Log in or Sign up"):
        st.login("auth0")
    st.stop()

# Logout button
if st.sidebar.button("Log out"):
    st.logout()
    st.session_state['user_type'] = None
    st.session_state['username'] = None
    st.stop()  

# Initialize session state
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "username" not in st.session_state:
    st.session_state.username = None

# Only access user info if available
if hasattr(st.experimental_user, "email"):
    conn = create_connection()
    if conn is not None:
        create_table(conn)

        # Check if user exists
        user_data = get_user(conn, st.experimental_user.email)
        if user_data is not None:
            st.session_state['user_type'] = user_data[3]
            st.session_state['username'] = user_data[1]
        else:
            user_type = 'guest'
            username = st.experimental_user.email
            st.session_state['user_type'] = user_type
            st.session_state['username'] = username
            insert_user(conn, username, st.experimental_user.email, user_type)

# Show menu
menu()