import streamlit as st

# This file contains the menu functions for the AIFAQ application.
# It provides a navigation menu for authenticated users and a different menu for unauthenticated users.
# The menu is displayed in the sidebar of the Streamlit application.
def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/chatbot.py", label="AIFAQ ChatBot")
    if st.session_state.user_type in ["admin"]:
        st.sidebar.page_link("pages/config_page_public.py", label="Config Public Page")
        st.sidebar.page_link("pages/config_page_private.py", label="Config Private Page")
        st.sidebar.page_link("pages/build_knowledgebase.py", label="Build Knowledge Base")
    st.sidebar.page_link("app.py", label="About")

# This function is called when the user is not authenticated.
# It shows a simplified navigation menu with only the About page.
def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="About")

# This function is called to display the menu based on the user's authentication status.
# It checks if the user is logged in and shows the appropriate menu.
def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "user_type" not in st.session_state or st.session_state.user_type is None:
        unauthenticated_menu()
        return
    authenticated_menu()

# This function is called to redirect users to the main page if they are not logged in.
# It checks the session state for the user's authentication status and calls the menu function.
def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "user_type" not in st.session_state or st.session_state.user_type is None:
        st.switch_page("app.py")
    menu()