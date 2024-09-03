import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from model import load_quantized_model
from utils import load_yaml_file
from session_history import get_session_history

def initialize_models():
    config_data = load_yaml_file("config.yaml")
    tokenizer = AutoTokenizer.from_pretrained(config_data["model_name"])
    model = load_quantized_model(config_data["model_name"])
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    embeddings = HuggingFaceEmbeddings(model_name=config_data["embedding_model_name"])
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=config_data["persist_directory"]
    )
    return model, tokenizer, vectordb

def retrieve_relevant_context(query, vectordb, top_k=3):
    results = vectordb.similarity_search(query, k=top_k)
    return "\n".join([doc.page_content for doc in results])

def contextualize_question(query, conversation_history):
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    contextualized_query = contextualize_q_prompt.format(chat_history=conversation_history, input=query)
    return contextualized_query

def generate_response(session_id, model, tokenizer, query, vectordb):
    conversation_history = get_session_history(session_id)
    contextualized_query = contextualize_question(query, conversation_history.messages)
    
    context = retrieve_relevant_context(contextualized_query, vectordb)

    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use five sentences maximum and keep the answer concise."""
    
    full_prompt = f"{qa_system_prompt}\n\nContext: {context}\n\nQuestion: {contextualized_query}\n\nAnswer:"
    inputs = tokenizer(full_prompt, return_tensors="pt", padding=True).to(model.device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=1000,
        do_sample=True,
        temperature=0.7
    )

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    response = ""
    for token in streamer:
        yield token
        response += token
    
    conversation_history.add_user_message(query)
    conversation_history.add_ai_message(response)

