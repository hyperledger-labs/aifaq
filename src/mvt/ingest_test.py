import os
from os.path import isfile, join
from os import listdir
from utils import load_yaml_file, bs4_extractor
from dotenv import load_dotenv, find_dotenv
#from transformers import AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders.youtube import YoutubeLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_community.document_loaders import ReadTheDocsLoader

# Read config data
config_data = load_yaml_file("config.yaml")

# load environment variables
load_dotenv(find_dotenv())

# get mistral api key
api_key = os.getenv("MISTRALAI_API_KEY")

dataset_dir = config_data["dataset_path"]

yt_list = []

# read folder: files contain urls
folder_pth = join(dataset_dir, config_data["yt_video_links"])
files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

# read each file in yt folder
for file in files:
    fpath = os.path.join(folder_pth, file)
    with open(fpath, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            url = line.rstrip()
            try:
                loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
                yt_list.append(loader)
            except:
                print("Invalid url: " + url)

web_list = []

# read folder: files contain urls
folder_pth = join(dataset_dir, config_data["web_urls"])
files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

# read each file in web folder
for file in files:
    fpath = os.path.join(folder_pth, file)
    with open(fpath, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            url = line.rstrip()
            try:
                loader = RecursiveUrlLoader(url=url, extractor=bs4_extractor, prevent_outside=True)
                web_list.append(loader)
            except:
                print("Invalid url: " + url)

# read folder that contains pdf files
folder_pth = join(dataset_dir, config_data["pdf_files"])
pdf_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

# read and parse each file in pdf folder
pdf_list = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path=folder_pth,
        glob="*.pdf",
    ),
    blob_parser=PyPDFParser(),
)

# read folder that contains readthedocs files
folder_pth = join(dataset_dir, config_data["rtdocs_files"])
rtdocs_list = ReadTheDocsLoader(folder_pth, encoding="utf-8")

# read folder that contains text files
folder_pth = join(dataset_dir, config_data["text_files"])

# avoid exception opening the files
text_loader_kwargs={'autodetect_encoding': True}
txt_list = DirectoryLoader(folder_pth, glob="*.txt", loader_cls=TextLoader, show_progress=True, loader_kwargs=text_loader_kwargs)

# list of loaders
loaders = []

for item in web_list:
    loaders.append(item)

for item in yt_list:
    loaders.append(item)

loaders.append(pdf_list)

loaders.append(rtdocs_list)

loaders.append(txt_list)

# merge all the document sources
loader= MergedDataLoader(loaders=loaders)

# Load data
docs = loader.load()


# We use a hierarchical list of separators specifically tailored for splitting Markdown documents
# This list is taken from LangChain's MarkdownTextSplitter class
MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]

chunk_size = 512

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,  # The maximum number of characters in a chunk: we selected this value arbitrarily
    chunk_overlap=int(chunk_size/10),  # The number of characters to overlap between chunks
    add_start_index=True,  # If `True`, includes chunk's start index in metadata
    strip_whitespace=True,  # If `True`, strips whitespace from the start and end of every document
    separators=MARKDOWN_SEPARATORS,
)

docs_processed = []
for doc in docs:
    docs_processed += text_splitter.split_documents([doc])


for doc in docs_processed:
  print(doc, file=open('document_text.txt', 'a', encoding='utf-8'))

# Define the embedding model
embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=api_key)

# Create the vector store 
vectordb = FAISS.from_documents(docs_processed, embeddings)
# Save local vector db 
vectordb.save_local(config_data["persist_directory"])