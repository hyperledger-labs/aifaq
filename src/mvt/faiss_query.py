import os
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings

# Read config data
config_data = load_yaml_file("config.yaml")

load_dotenv(find_dotenv())

api_key = os.getenv("MISTRALAI_API_KEY")

# Define the embedding model
embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=api_key)

# Load local vector db
docsearch = FAISS.load_local(config_data["persist_directory"], embeddings, allow_dangerous_deserialization=True)

retriever = docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 4})
results = retriever.invoke("I'd like to launch a new startup, do you suggest to me to join the FI program?")

# save response in a text file
print(results, file=open('responses.txt', 'a', encoding='utf-8'))