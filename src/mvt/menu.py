import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Homepage")
    st.sidebar.page_link("pages/chatbot.py", label="AIFAQ ChatBot")
    if st.session_state.roles in ["admin"]:
        st.sidebar.page_link("pages/config_page.py", label="Config Page")
        st.sidebar.page_link("pages/build_knowledgebase.py", label="Build Knowledge Base")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Homepage")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "roles" not in st.session_state or st.session_state.roles is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "roles" not in st.session_state or st.session_state.roles is None:
        st.switch_page("app.py")
    menu()