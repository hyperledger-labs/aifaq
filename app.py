import streamlit as st
from menu import menu, unauthenticated_menu
from database import create_connection, create_table, get_user, insert_user
from homepage import gethomepage

# Get markdown homepage
st.markdown(body=gethomepage(), unsafe_allow_html=True)

# Initialize session state for user_type and username
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "username" not in st.session_state:
    st.session_state.username = None

# Check if user is authenticated
if st.user.is_logged_in:
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        user_data = get_user(conn, st.user.email)
        if user_data is not None:
            st.session_state['user_type'] = user_data[3]
            st.session_state['username'] = user_data[1]
        else:
            user_type = 'guest'
            username = st.user.email
            st.session_state['user_type'] = user_type
            st.session_state['username'] = username
            insert_user(conn, username, st.user.email, user_type)
    
    # Show authenticated menu
    menu()
    
else:
    st.session_state['user_type'] = 'guest'
    st.session_state['username'] = 'guest'
    
    if st.button("Log in or Sign up"):
        st.login("auth0")
    
    # Show menu for unauthenticated users, which will now have a link to the chatbot
    unauthenticated_menu()