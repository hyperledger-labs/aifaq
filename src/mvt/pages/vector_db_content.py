import streamlit as st
import os
from utils import load_yaml_file_with_db_prompts
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from menu import menu_with_redirect

menu_with_redirect()

# only allow admin users
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Vector DB Content (FAISS)")

# load the configuration and environment variables
config_data = load_yaml_file_with_db_prompts("config.yaml")
load_dotenv(find_dotenv())

# set up the embeddings model based on the provider
if config_data["llm_provider"] == "mistral":
    embeddings = MistralAIEmbeddings(
        model=config_data["embedding_model"],
        mistral_api_key=os.getenv("MISTRALAI_API_KEY")
    )
else:
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# load the FAISS vector database from disk
persist_dir = config_data["persist_directory"]
try:
    vectordb = FAISS.load_local(
        persist_dir,
        embeddings,
        allow_dangerous_deserialization=True
    )
    st.success(f"Loaded FAISS content from '{persist_dir}'")
except Exception as e:
    st.error(f"Could not load FAISS content: {e}")
    st.stop()

# get all documents from the vector database (may be slow if many documents)
try:
    all_docs = list(vectordb.docstore._dict.values())
except Exception as e:
    st.error(f"Could not access documents in FAISS index: {e}")
    st.stop()

search_term = st.text_input("Search in vector DB content:", "")

# Check if a document matches the search term 
def doc_matches(doc, term):
    if not term:
        return True
    terms = [t.strip().lower() for t in term.split() if t.strip()]
    content = getattr(doc, 'page_content', '').lower()
    metadata_values = [str(v).lower() for v in getattr(doc, 'metadata', {}).values()]
    for t in terms:
        if t not in content and not any(t in v for v in metadata_values):
            return False
    return True

filtered_docs = [doc for doc in all_docs if doc_matches(doc, search_term)]

st.markdown(f"### Showing {len(filtered_docs)} / {len(all_docs)} documents")

# show each document with its metadata and a snippet of its content
for i, doc in enumerate(filtered_docs):
    with st.expander(f"Document {i+1}"):
        st.write("**Metadata:**", doc.metadata)
        snippet = doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else "")
        st.write("**Content snippet:**")
        st.code(snippet)
        with st.expander("Show full content"):
            st.write(doc.page_content)
