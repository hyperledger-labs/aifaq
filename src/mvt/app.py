import streamlit as st
from menu import menu
from database import create_connection, create_table, get_user, insert_user
from homepage import gethomepage
from auth0_component import login_button

# Get markdown homepage
st.markdown(body=gethomepage(), unsafe_allow_html=True)

# Auth0 configuration
AUTH0_CLIENT_ID = "efqtkHTVVQtsBIM86BGMf1VfyVtiyc01"
AUTH0_DOMAIN = "dev-tz87kqmkwnpatla6.us.auth0.com"
AUTH0_REDIRECT_URI = "http://localhost:8501"

user_info = login_button(AUTH0_CLIENT_ID, domain = AUTH0_DOMAIN)

if user_info:
    st.success(f"Welcome {user_info['name']}!")
    st.write("🔐 You are logged in.")
    st.write("📧 Email:", user_info['email'])
    st.write("🆔 Sub:", user_info['sub'])

    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.experimental_rerun()
else:
    st.warning("Please log in to continue.")


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