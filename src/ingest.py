import sys
import os
from os.path import isfile, join
from os import listdir
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from ingest_process import get_vectordb

# the received argument is the loggedin user and the documents' owner
owner = sys.argv[1]

# Read config data
config_data = load_yaml_file("config.yaml")

# load environment variables
load_dotenv(find_dotenv())

public_dataset_dir = config_data["dataset_public_path"]
private_dataset_dir = config_data["dataset_private_path"]

public_vectordb = get_vectordb(owner, "public", datasetdir=public_dataset_dir)
private_vectordb = get_vectordb(owner, "private", datasetdir=private_dataset_dir)

# Save local vector db 
if public_vectordb is not None and private_vectordb is not None: 
  public_vectordb.merge_from(private_vectordb)
  public_vectordb.save_local(config_data["persist_directory"])
elif public_vectordb is None and private_vectordb is not None:
  private_vectordb.save_local(config_data["persist_directory"])
else: 
  public_vectordb.save_local(config_data["persist_directory"])