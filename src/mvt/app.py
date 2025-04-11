import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from menu import menu

st.set_page_config(layout="wide")

# Load the config
with open('./credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    auth = authenticator.login('main')
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
    # Stop the rendering if the user isn't connected
    st.stop()
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
    # Stop the rendering if the user isn't connected
    st.stop()
elif st.session_state["authentication_status"]: # All the authentication info is stored in the session_state
    # User is connected    
    username = st.session_state['username']
    role = st.session_state['roles']

    st.markdown(
        f"""
        <div style='text-align: center; padding: 0px 0px;'>
            <p style='font-size: 30px; margin-bottom: 0;'>Hey {username}👋</p>
            <p style='font-size: 20px; color: gray; margin-top: 5px;'>role: <strong>{role}</strong></p>
            <h1 style='font-size: 54px; margin-bottom: 0;'>Welcome to AIFAQ</h1>
            <p style='font-size: 18px; max-width: 600px; margin: auto; padding-bottom:50px;'>
                An <strong>AI-powered chatbot</strong> built for <em>document Q&A</em>  powered by <a href='https://github.com/hyperledger-labs/aifaq' target='_blank' style='color: teal; text-decoration: none;'>Hyperledger Labs</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([5,1,5])
    with col2:
        authenticator.logout('Logout', 'main')

# Initialize st.session_state.role to None
if "roles" not in st.session_state:
    st.session_state.roles = None

menu() # Render the dynamic menu!