import streamlit as st
from menu import menu, unauthenticated_menu
from database import create_connection, create_table, get_user, insert_user
from homepage import gethomepage
from utils import load_yaml_file

# Load configuration
config = load_yaml_file("config.yaml")
demo = config.get("demo_mode", False)

# Homepage markdown
st.markdown(body=gethomepage(), unsafe_allow_html=True)

# Initialize session state
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "username" not in st.session_state:
    st.session_state.username = None

# DEMO MODE → bypass authentication entirely
if demo:
    st.session_state['user_type'] = "guest"
    st.session_state['username'] = "guest"
    unauthenticated_menu()
    st.info("Running in DEMO MODE - Login disabled.")
    st.stop()

# FULL AUTH MODE
if hasattr(st, "user") and getattr(st.user, "is_logged_in", False):

    conn = create_connection()
    if conn is not None:
        create_table(conn)
        user_data = get_user(conn, st.user.email)

        if user_data is not None:
            st.session_state['user_type'] = user_data[3]
            st.session_state['username'] = user_data[1]
        else:
            user_type = 'user'
            username = st.user.email
            st.session_state['user_type'] = user_type
            st.session_state['username'] = username
            insert_user(conn, username, st.user.email, user_type)

    menu()

else:
    st.session_state['user_type'] = "guest"
    st.session_state['username'] = "guest"
    unauthenticated_menu()
