from utils import load_yaml_file, escape_markdown
from main import get_ragchain
import streamlit as st
from menu import menu, unauthenticated_menu
from chat_history import init_db, save_message, get_messages, on_feedback_change
from query_rewriting import query_rewriting_llm
import uuid

# Initialize DB
init_db()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "user_type" not in st.session_state:
    if st.user.is_logged_in:
        st.session_state.user_type = "user"
        st.session_state.username = st.user.email
    else:
        st.session_state.user_type = "guest"
        st.session_state.username = "guest"

# Gestione del menu basata sullo stato di autenticazione
if st.user.is_logged_in:
    menu()
else:
    unauthenticated_menu()

# --- Get Client IP (Streamlit 1.47.0 + NGINX) ---
def get_client_ip():
    try:
        headers = st.context.headers

        # Nginx will pass this correctly
        ip = headers.get("x-real-ip")

        # Fallback: first element of X-Forwarded-For
        if not ip:
            xff = headers.get("x-forwarded-for")
            if xff:
                ip = xff.split(",")[0].strip()

        return ip or "unknown"
    except Exception as e:
        return f"error: {e}"

client_ip = get_client_ip()
st.session_state["client_ip"] = client_ip

st.markdown(f"**Your IP:** {client_ip}")
# ------------------------------------------------


config_path = "./config.yaml"
logo_path = "https://github.com/hyperledger-labs/aifaq/blob/mvt-streamlit/images/logo.png?raw=true"
config_data = load_yaml_file(config_path)

title = config_data["company_name"]
title = "# " + title if title else "# AIFAQ"
st.markdown(title)

# guest users have access only to public documents
filter = None
if st.session_state.user_type in ['guest']:
    filter = {"access": {"$eq": "public"}}

rag_chain = get_ragchain(filter)
username = st.session_state.username

def create_initial_message(username: str):
    # create and save the initial welcome message
    msg_id = save_message(username, "assistant", "How may I help you?", st.session_state.session_id)
    return [{
        "id": msg_id,
        "role": "assistant",
        "content": "How may I help you?",
        "feedback": None
    }]

# Load user chat history or initialize it
if "user_messages" not in st.session_state:
    st.session_state.user_messages = {}

if st.session_state.user_type in ['guest']:
    # Do not load from DB for guest users
    messages = st.session_state.user_messages.get(username, [])
    if not messages:
        messages = create_initial_message(username)
else:
    # Normal users → load from DB
    messages = get_messages(username)
    if not messages:
        messages = create_initial_message(username)

# Update session state
st.session_state.user_messages[username] = messages
user_chat = st.session_state.user_messages[username]


# fragment allows to reder only the messages without reloading the whole page
@st.fragment
def render_message(message):
    with st.chat_message(message["role"], avatar=logo_path if message["role"] == "assistant" else None):
        st.markdown(escape_markdown(message["content"]))
        
        # Feedback only for assistant messages
        if message["role"] == "assistant":
            message_id = message.get("id")

            if message_id is not None:
                fb_key = f"feedback_{message_id}"

            if fb_key not in st.session_state:
                st.session_state[fb_key] = message.get("feedback", None)

            st.feedback(
                config_data["feedback_options"],
                key=fb_key,
                disabled=st.session_state.get(fb_key) is not None, # Disable if feedback already given
                on_change=on_feedback_change,
                args=(message_id, fb_key)
            )

# -------------------------------
# Display chat messages
# -------------------------------
for message in user_chat:
    render_message(message)

# -------------------------------
# Handle user input
# -------------------------------
if prompt := st.chat_input():
    msg_id = save_message(username, "user", prompt, st.session_state.session_id)
    msg = {"id": msg_id, "role": "user", "content": prompt, "feedback": None}
    user_chat.append(msg)

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        query = query_rewriting_llm(prompt) if config_data.get("use_query_rewriting", True) else prompt
        response = rag_chain.invoke({"input": query})
        print(response, file=open('responses.txt', 'a', encoding='utf-8'))

    reply_id = save_message(username, "assistant", response["answer"], st.session_state.session_id)
    reply_msg = {"id": reply_id, "role": "assistant", "content": response["answer"], "feedback": None}
    user_chat.append(reply_msg)
    render_message(reply_msg) # render the last message to show the feedback button
