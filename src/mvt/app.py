import streamlit as st
from menu import menu
from database import create_connection, create_table, create_prompts_table, get_user, insert_user
from homepage import gethomepage
import os
import sys
from dotenv import load_dotenv, find_dotenv

# Load environment variables FIRST, before any imports
load_dotenv(find_dotenv())

# Set HF_TOKEN in environment
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ["HF_TOKEN"] = hf_token
else:
    print("WARNING: HF_TOKEN not found in environment variables")

# Check command line arguments for mode
def get_operation_mode():
    """Determine operation mode from command line arguments or session state override"""
    # Check if user switched to dev mode via button
    if st.session_state.get("switch_to_dev", False):
        return "dev"
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        return "dev"
    return "production"

# Define the mode of operation
operation_mode = get_operation_mode()

# Function to check if production credentials are configured
def check_production_credentials():
    """Check if required credentials are configured in secrets.toml"""
    try:
        # Check if auth0 credentials are configured
        auth0_domain = st.secrets.get("auth.auth0.domain", "")
        auth0_client_id = st.secrets.get("auth.auth0.client_id", "")
        auth0_client_secret = st.secrets.get("auth.auth0.client_secret", "")
        
        # Check if google credentials are configured
        google_client_id = st.secrets.get("auth.google.client_id", "")
        google_client_secret = st.secrets.get("auth.google.client_secret", "")
        
        # Return True if at least one authentication method is configured
        return bool(auth0_domain and auth0_client_id and auth0_client_secret) or \
               bool(google_client_id and google_client_secret)
    except Exception:
        return False

# Function to display error message
def show_credentials_error():
    """Display error message for missing credentials"""
    st.error("⚠️ Production Mode Error: Credentials not configured")
    
    st.write("You're trying to run the application in **production mode**, but the required authentication credentials are not configured in your `.streamlit/secrets.toml` file.")
    
    st.subheader("Solutions:")
    
    st.write("**Option 1: Use Development Mode**")
    st.code("streamlit run app.py dev")
    
    st.write("**Option 2: Fill up credentials in secrets.toml for Production**")
    st.write("For production mode, you need to fill up the credentials in your `.streamlit/secrets.toml` file:")
    
    st.code("""
# For Auth0 authentication
[auth.auth0]
domain = "your-domain.auth0.com"
client_id = "your-client-id"
client_secret = "your-client-secret"
server_metadata_url = "https://your-domain.auth0.com/.well-known/openid_configuration"
client_kwargs = { "prompt" = "login"}

# OR for Google OAuth
[auth.google]
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"

# General auth settings
[auth]
redirect_uri = "your-redirect-uri"
cookie_secret = "your-cookie-secret"
""")
    
    st.warning("⚠️ **For Production Mode:** Either fill up the credentials in `secrets.toml` or use dev mode by running `streamlit run app.py dev`")

# Check if we're in production mode and credentials are missing
if operation_mode == "production" and not check_production_credentials():
    show_credentials_error()
    # Don't stop here, let the button work
    if st.button("🔄 Switch to Development Mode", type="primary"):
        # Set a session state to indicate dev mode switch
        st.session_state.switch_to_dev = True
        st.rerun()
    
    # Only stop if user hasn't clicked the switch button
    if not st.session_state.get("switch_to_dev", False):
        st.stop()

# Get markdown homepage
st.markdown(body=gethomepage(), unsafe_allow_html=True)

# Display current mode indicator
if operation_mode == "dev":
    st.sidebar.info("Development Mode")
else:
    st.sidebar.success("Production Mode")

if (operation_mode == "dev"):
    # Development mode: no authentication required
    # Initialize all necessary session state variables for full functionality
    if "user_type" not in st.session_state:
        st.session_state.user_type = "admin"  # Set to admin for full access
    if "username" not in st.session_state:
        st.session_state.username = "dev@example.com"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True
    if "email" not in st.session_state:
        st.session_state.email = "dev@example.com"
else:
    # Production mode: check if user is authenticated
    # Check if user is authenticated
    if not st.experimental_user.is_logged_in:
        if st.button("Log in or Sign up"):
            st.login("auth0")
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
            create_prompts_table(conn)

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

# Initialize database tables in dev mode as well
if operation_mode == "dev":
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        create_prompts_table(conn)
        conn.close()

# Show menu
menu()