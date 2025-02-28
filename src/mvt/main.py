import os
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_mistralai.embeddings import MistralAIEmbeddings

def get_ragchain():
  

    # Read config data
    config_data = load_yaml_file("config.yaml")

    load_dotenv(find_dotenv())

    api_key = os.getenv("MISTRALAI_API_KEY")

    # Define the embedding model
    embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=api_key)

    # Load local vector db
    docsearch = FAISS.load_local(config_data["persist_directory"], embeddings, allow_dangerous_deserialization=True)

    # Define a retriever interface
    retriever = docsearch.as_retriever()

    # Define LLM
    model = ChatMistralAI(mistral_api_key=api_key, model=config_data["model_name"])

    # Answer question
    qa_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use five sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)  

    return rag_chain