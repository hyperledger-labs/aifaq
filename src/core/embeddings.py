import torch
from utils import load_yaml_file
from langchain_huggingface import HuggingFaceEmbeddings

def embedding_function():
    config_data = load_yaml_file("config.yaml")
    
    # check if GPU is available, else use CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_name = config_data["embedding_model_name"]
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    return embeddings