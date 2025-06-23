import os
from utils import load_yaml_file_with_db_prompts
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_mistralai.embeddings import MistralAIEmbeddings
#from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.documents import Document
from typing import List


def get_ragchain(filter):
    # Read config data with database prompt overrides
    config_data = load_yaml_file_with_db_prompts("config.yaml")
    load_dotenv(find_dotenv())

    # Get API keys
    mistral_api_key = os.getenv("MISTRALAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Select embeddings and LLM based on provider
    if config_data["llm_provider"] == "mistral":
        embeddings = MistralAIEmbeddings(
            model=config_data["embedding_model"], 
            mistral_api_key=mistral_api_key
        )
        model = ChatMistralAI(
            mistral_api_key=mistral_api_key,
            model=config_data["model_name"]
        )
    else:  # default to OpenAI
        from langchain_openai import ChatOpenAI
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key
        )
        model = ChatOpenAI(
            openai_api_key=openai_api_key,
            model=config_data["model_name"],
            temperature=0.7
        )
    
    # Load local vector db
    docsearch = FAISS.load_local(config_data["persist_directory"], embeddings, allow_dangerous_deserialization=True)

    # Define a retriever interface
    retriever = docsearch.as_retriever(search_kwargs={"k": 5, "filter": filter})

    # read prompt string from config file
    prompt_str = config_data["system_prompt"]

    # Answer question
    qa_system_prompt = (
    prompt_str +
    "\n\n"
    "{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            ("user", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)  

    return rag_chain