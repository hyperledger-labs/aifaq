from utils import load_yaml_file, escape_markdown
from main import get_ragchain
import streamlit as st
from menu import menu, unauthenticated_menu
from chat_history import init_db, save_message, get_messages, on_feedback_change
from query_rewriting import query_rewriting_llm

# Initialize DB
init_db()

# Gestione del menu basata sullo stato di autenticazione
if st.user.is_logged_in:
    menu()
else:
    unauthenticated_menu()

config_path = "./config.yaml"
logo_path = "https://github.com/hyperledger-labs/aifaq/blob/mvt-streamlit/images/logo.png?raw=true"
config_data = load_yaml_file(config_path)

title = config_data["company_name"]
title = "# " + title if title else "# AIFAQ"
st.markdown(title)

# filter public document in case of guest user
filter = None
if st.session_state.user_type in ['guest']:
    filter = {"access": {"$eq": "public"}}

rag_chain = get_ragchain(filter)
username = st.session_state.username

def create_initial_message(username: str):
    """Crea e salva il messaggio iniziale di benvenuto."""
    msg_id = save_message(username, "assistant", "How may I help you?")
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
    msg_id = save_message(username, "user", prompt)
    msg = {"id": msg_id, "role": "user", "content": prompt, "feedback": None}
    user_chat.append(msg)

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        query = query_rewriting_llm(prompt) if config_data.get("use_query_rewriting", True) else prompt
        response = rag_chain.invoke({"input": query})
        print(response, file=open('responses.txt', 'a', encoding='utf-8'))

    reply_id = save_message(username, "assistant", response["answer"])
    reply_msg = {"id": reply_id, "role": "assistant", "content": response["answer"], "feedback": None}
    user_chat.append(reply_msg)
    render_message(reply_msg) # render the last message to show the feedback button

