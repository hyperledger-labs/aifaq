
import os
from pathlib import Path
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from transformers import AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders import ReadTheDocsLoader



# Read config data
config_data = load_yaml_file("config.yaml")

# load environment variables
load_dotenv(find_dotenv())

# get mistral api key
api_key = os.getenv("MISTRALAI_API_KEY")

# load documents from urls
loader_web = RecursiveUrlLoader(url=config_data["wiki_url"])

# load documents from ReadTheDocs documentation
loader_rtdocs = ReadTheDocsLoader(path="./rtdocs", encoding="utf-8", patterns=("*.html"))

# merge all the document sources
loader= MergedDataLoader(loaders=[loader_rtdocs, loader_web])

# Load data
docs = loader.load()

# Split text into chunks 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(docs)

# Define the embedding model
embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=api_key)

# Create the vector store 
vectordb = FAISS.from_documents(documents, embeddings)
# Save local vector db 
vectordb.save_local(config_data["persist_directory"])