import streamlit as st
from utils import load_yaml_file

# Read config data
config_data = load_yaml_file("config.yaml")

def handle_logout():
    """Handle logout action and state cleanup"""
    if st.sidebar.button("Log out"):
        st.session_state['user_type'] = None
        st.session_state['username'] = None
        st.session_state.pop('first_login', None)
        st.logout()
        st.switch_page("app.py")

def authenticated_menu():
    # Show logout button at the top of sidebar
    handle_logout()
    
    # Show a navigation menu for authenticated users
    chatbot_label = config_data["company_name"] + " ChatBot"
    st.sidebar.page_link("pages/chatbot.py", label=chatbot_label)
    if st.session_state.user_type in ["admin"]:
        st.sidebar.page_link("pages/config_page_public.py", label="Config Public Page")
        st.sidebar.page_link("pages/config_page_private.py", label="Config Private Page")
        st.sidebar.page_link("pages/build_knowledgebase.py", label="Build Knowledge Base")
        st.sidebar.page_link("pages/user_management.py", label="User Management")
        st.sidebar.page_link("pages/analytics.py", label="Analytics")
    st.sidebar.page_link("app.py", label="About")
    st.sidebar.markdown(
        f"[Contact us]({config_data['contact_page']})",
        unsafe_allow_html=True
    )
 

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="About")

def menu():
    # Check authentication status
    if "user_type" not in st.session_state or st.session_state.user_type is None:
        unauthenticated_menu()
        return

    # Redirect to chatbot on first successful login
    if "first_login" not in st.session_state:
        st.session_state.first_login = True
        st.switch_page("pages/chatbot.py")
    
    authenticated_menu()

def menu_with_redirect():
    if "user_type" not in st.session_state or st.session_state.user_type is None:
        st.switch_page("app.py")
    menu()