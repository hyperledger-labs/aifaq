import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from menu import menu

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
    authenticator.logout('Logout', 'main') 

# Initialize st.session_state.role to None
if "roles" not in st.session_state:
    st.session_state.roles = None

st.write("AIFAQ is an AI chatbot powered by https://github.com/hyperledger-labs/aifaq")

st.write(f"You are logged in as {st.session_state['username']}")
st.write(f"Your role is {st.session_state.roles}")

menu() # Render the dynamic menu!