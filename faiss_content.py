import os
from utils import load_yaml_file
#from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# Read config data
try:
    config_data = load_yaml_file("../config.yaml")
except FileNotFoundError:
    try:
        config_data = load_yaml_file("./config.yaml")
    except FileNotFoundError:
        raise FileNotFoundError("Could not find config.yaml in either ../ or ./ directories")

load_dotenv(find_dotenv())

# Get API keys
mistral_api_key = os.getenv("MISTRALAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Select embeddings based on provider
if config_data["llm_provider"] == "mistral":
    embeddings = MistralAIEmbeddings(
        model=config_data["embedding_model"],
        mistral_api_key=mistral_api_key
    )
else:  # default to OpenAI
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key
    )

docsearch = FAISS.load_local(f"./{config_data['persist_directory']}", embeddings, allow_dangerous_deserialization=True)

"""

# Load local vector db
try:
    docsearch = FAISS.load_local(config_data["persist_directory"], embeddings, allow_dangerous_deserialization=True)
except FileNotFoundError:
    try:
        docsearch = FAISS.load_local(f"../{config_data['persist_directory']}", embeddings, allow_dangerous_deserialization=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find vector store in either {config_data['persist_directory']} or ../{config_data['persist_directory']}")
"""

print(docsearch.docstore._dict)

# save data in a text file
print(docsearch.docstore._dict, file=open('vectordb.txt', 'a', encoding='utf-8'))
