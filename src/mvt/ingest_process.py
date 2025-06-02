import os
from os.path import isfile, join
from os import listdir
from utils import load_yaml_file, bs4_extract_linear_text, extract_video_id, save_transcript
from dotenv import load_dotenv, find_dotenv
#from transformers import AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import BSHTMLLoader
from langchain_openai import OpenAIEmbeddings

# This function builds a knowledge base by loading various document types from specified directories.
# It processes YouTube links, web URLs, PDF files, HTML files, and text files
def get_vectordb(owner: str, access: str, datasetdir: str):
  config_data = load_yaml_file("config.yaml")

  # load environment variables
  load_dotenv(find_dotenv())

  dataset_dir = datasetdir

  yt_list = []

  # read folder: files contain yt links
  folder_pth = join(dataset_dir, config_data["yt_video_links"])
  yt_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

  # read each file in yt folder
  for file in yt_files:
      fpath = os.path.join(folder_pth, file)
      with open(fpath, 'r', encoding='UTF-8') as file:
          while line := file.readline():
              url = line.rstrip()
              # extract video id from url
              id_video = extract_video_id(url)
              try:
                  out_path = os.path.join(folder_pth, "./transcripts")
                  save_transcript(id_video, out_path)
              except:
                  print("Invalid url: " + url)


  # avoid exception opening the files
  out_path = os.path.join(folder_pth, "transcripts")
  if os.path.exists(out_path):
      text_loader_kwargs={'autodetect_encoding': True}
      yt_list = DirectoryLoader(out_path, glob="*", loader_cls=TextLoader, show_progress=True, loader_kwargs=text_loader_kwargs)
  else:
      print("folder does not exist: " + out_path)
      

  web_list = []

  # read folder: files contain urls
  folder_pth = join(dataset_dir, config_data["web_urls"])
  web_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

  # read each file in web folder
  for file in web_files:
      fpath = os.path.join(folder_pth, file)
      with open(fpath, 'r', encoding='UTF-8') as file:
          while line := file.readline():
              url = line.rstrip()
              try:
                  loader = RecursiveUrlLoader(url=url, extractor=bs4_extract_linear_text, prevent_outside=True)
                  web_list.append(loader)
              except:
                  print("Invalid url: " + url)


  # read folder that contains pdf files
  folder_pth = join(dataset_dir, config_data["pdf_files"])

  # read and parse each file in pdf folder
  pdf_list = GenericLoader(
      blob_loader=FileSystemBlobLoader(
          path=folder_pth,
          glob="*.pdf",
      ),
      blob_parser=PyPDFParser(),
  )

  html_list = []

  # read folder that contains html files
  folder_pth = join(dataset_dir, config_data["html_files"])
  html_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]

  # read each file in html folder
  for file in html_files:
      fpath = os.path.join(folder_pth, file)
      try:
          loader = BSHTMLLoader(fpath, open_encoding='utf-8')
          html_list.append(loader)
      except:
          print("Invalid html file: " + fpath)


  # read folder that contains readthedocs files
  folder_pth = join(dataset_dir, config_data["rtdocs_files"])
  rtdocs_list = ReadTheDocsLoader(folder_pth, encoding="utf-8")

  # read folder that contains text files
  folder_pth = join(dataset_dir, config_data["text_files"])

  # avoid exception opening the files
  text_loader_kwargs={'autodetect_encoding': True}
  txt_list = DirectoryLoader(folder_pth, glob="*", loader_cls=TextLoader, show_progress=True, loader_kwargs=text_loader_kwargs)

  # list of loaders
  loaders = []
  

  for item in web_list:
      loaders.append(item)
      
  for item in html_list:
      loaders.append(item)
  
  loaders.append(pdf_list)

  loaders.append(rtdocs_list)

  if yt_list:
      loaders.append(yt_list)

  loaders.append(txt_list)
  
  
  # merge all the document sources
  loader= MergedDataLoader(loaders=loaders)

  # Load data
  docs = loader.load()

  # set document owner and access type
  for doc in docs:
      doc.metadata.update({'owner':owner, 'access': access})

  # Split text into chunks 
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  documents = text_splitter.split_documents(docs)

  # Get API keys
  mistral_api_key = os.getenv("MISTRALAI_API_KEY")
  openai_api_key = os.getenv("OPENAI_API_KEY")

  # Select embeddings based on provider
  if config_data["llm_provider"] == "mistral":
    embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=mistral_api_key)
  else:  # default to OpenAI
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

  if documents:
    # Create the vector store 
    vectordb = FAISS.from_documents(documents, embeddings)
    return vectordb
  else:
    return None