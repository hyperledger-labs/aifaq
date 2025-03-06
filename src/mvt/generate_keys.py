import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load the config
with open('./credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

# Save the Hashed Credentials to our config file
with open('./credentials.yml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)