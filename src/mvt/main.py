import os
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
#from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.documents import Document
from typing import List


def rerank_documents(query: str, documents: List[Document], embeddings, top_k: int = 5) -> List[Document]:
    """Rerank documents using cosine similarity"""
    query_embedding = embeddings.embed_query(query)
    doc_embeddings = [embeddings.embed_query(doc.page_content) for doc in documents]
    
    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    
    # Create list of (doc, score) tuples and sort by score
    doc_scores = list(zip(documents, similarities))
    doc_scores.sort(key=lambda x: x[1], reverse=True)

def get_ragchain(filter):
    # Read config data
    config_data = load_yaml_file("config.yaml")
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
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 5, "filter": filter})

    """

    # Get documents for BM25
    documents = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in docsearch.docstore._dict.values()
    ]

    # Create BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 25  # Number of documents to retrieve

    # Create dense retriever from FAISS
    dense_retriever = docsearch.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 25, "filter": filter}
    )

    # Create ensemble retriever
    retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, dense_retriever],
        weights=[0.3, 0.7]  # Weight more towards dense retrieval
    )
"""
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