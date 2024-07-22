import os
import torch
from utils import load_yaml_file
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from embeddings import embedding_function

config_data = load_yaml_file("config.yaml")

persist_directory = config_data["persist_directory"]
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)
loader_web = RecursiveUrlLoader(url=config_data["url"])

loader_rtdocs = ReadTheDocsLoader(config_data["folder_path"], encoding="utf-8")

loader = MergedDataLoader(loaders=[loader_web, loader_rtdocs])

embeddings = embedding_function()

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

print(f"Number of chunks created: {len(splits)}")

vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_directory)
vectorstore.persist()

print("Vectorstore creation and persistence completed.")