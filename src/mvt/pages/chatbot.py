from utils import load_yaml_file
from main import get_ragchain
import streamlit as st
from menu import menu_with_redirect
from chat_history import init_db, save_message, get_messages
from query_rewriting import query_rewriting_llm
from database import create_connection, create_all_tables, insert_response, insert_document, link_document_response, get_document_by_source, get_user
import json

# Initialize DB
init_db()

# Initialize main database and create tables
conn = create_connection()
if conn:
    create_all_tables(conn)
    conn.close()

# Redirect to app.py if not logged in
menu_with_redirect()

st.markdown("# AIFAQ")

config_path = "./config.yaml"
logo_path = "https://github.com/hyperledger-labs/aifaq/blob/mvt-streamlit/images/logo.png?raw=true"
config_data = load_yaml_file(config_path)

# filter public document in case of guest user
filter = None
if st.session_state.user_type in ['guest']:
    filter = {"access": {"$eq": "public"}}


try:
    rag_chain = get_ragchain(filter)
except FileNotFoundError as e:
    st.error("⚠️ Knowledge base not initialized!")
    st.info("""
    The AI FAQ system needs to be set up first. Please:
    
    1. Add your documents/links to the Config public/private page first.
    2. Then update the knowledge base from Build Knowledge Base page.
    3. Then open this page again.
    
    Or contact an administrator to set up the knowledge base.
    """)
    st.stop()
except Exception as e:
    st.error(f"Error initializing the system: {str(e)}")
    st.stop()

username = st.session_state.username

# -------------------------------
# Load user chat history from DB
# -------------------------------
if "user_messages" not in st.session_state:
    st.session_state.user_messages = {}

if username not in st.session_state.user_messages:
    messages = get_messages(username)
    if not messages:
        messages = [{"role": "assistant", "content": "How may I help you?"}]
        save_message(username, "assistant", "How may I help you?")
    st.session_state.user_messages[username] = messages

user_chat = st.session_state.user_messages[username]

# -------------------------------
# Display chat messages
# -------------------------------
for message in user_chat:
    with st.chat_message(message["role"], avatar=logo_path if message["role"] == "assistant" else None):
        st.write(message["content"])

# -------------------------------
# Handle user input
# -------------------------------
if prompt := st.chat_input():
    msg = {"role": "user", "content": prompt}
    user_chat.append(msg)
    save_message(username, "user", prompt)

    with st.chat_message("user"):
        st.write(prompt)

    # Rewrite the query for better search
    rewritten_query = query_rewriting_llm(prompt)

    with st.chat_message("assistant", avatar=logo_path):
        with st.spinner("Thinking..."):
            # Use rewritten query or original prompt based on config
            query = rewritten_query if config_data.get("use_query_rewriting", True) else prompt
            response = rag_chain.invoke({"input": query})
            
            # Save response to database instead of text file
            conn = create_connection()
            if conn:
                try:
                    # Get user ID if logged in
                    user_id = None
                    if hasattr(st.session_state, 'email') and st.session_state.email:
                        user = get_user(conn, st.session_state.email)
                        user_id = user[0] if user else None
                    
                    # Insert response to database
                    response_id = insert_response(conn, response["answer"], query, user_id)
                    
                    # Process and save source documents
                    if response_id and "context" in response:
                        for doc in response["context"]:
                            # Extract source from document metadata
                            source = ""
                            if hasattr(doc, 'metadata') and doc.metadata:
                                source = doc.metadata.get('source', '')
                            elif hasattr(doc, 'page_content'):
                                source = f"content_{hash(doc.page_content) % 10000}"
                            
                            if source:
                                # Check if document already exists
                                existing_doc = get_document_by_source(conn, source)
                                if existing_doc:
                                    doc_id = existing_doc[0]
                                else:
                                    # Insert new document with metadata as JSON
                                    metadata_json = json.dumps(doc.metadata if hasattr(doc, 'metadata') and doc.metadata else {})
                                    doc_id = insert_document(conn, source, metadata_json)
                                
                                # Link document to response
                                if doc_id:
                                    link_document_response(conn, response_id, doc_id)
                    
                except Exception as e:
                    st.error(f"Error saving to database: {e}")
                finally:
                    conn.close()
            
            # Keep text file backup for now (can be removed later)
            print(response, file=open('responses.txt', 'a', encoding='utf-8'))
            st.markdown(response["answer"])

        reply_msg = {"role": "assistant", "content": response["answer"]}
        user_chat.append(reply_msg)
        save_message(username, "assistant", response["answer"])
