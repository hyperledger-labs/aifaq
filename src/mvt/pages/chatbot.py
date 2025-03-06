from utils import load_yaml_file
from main import get_ragchain
import streamlit as st
from menu import menu_with_redirect


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.markdown("# AIFAQ")

config_path = "config.yaml"

logo_path = "https://github.com/gcapuzzi/aifaq_streamlit/blob/main/logo.png?raw=true"

config_data = load_yaml_file(config_path)

rag_chain = get_ragchain()

prompt_to_user="How may I help you?"

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar=logo_path):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"], avatar=None):
            st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message(name='assistant', avatar=logo_path):
        with st.spinner("Thinking..."):
            response = rag_chain.invoke({"input": prompt}) 
            # save response in a text file
            print(response, file=open('responses.txt', 'a', encoding='utf-8'))
            st.markdown(response["answer"])
    message = {"role": "assistant", "content": response["answer"]}
    st.session_state.messages.append(message)