import torch
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.vectorstores import Chroma
from model import load_quantized_model
from tokenizer import initialize_tokenizer
from embeddings import embedding_function
from session_history import get_session_history
from utils import load_yaml_file

def get_conversation():
    config_data = load_yaml_file("config.yaml")

    model = load_quantized_model(config_data["model_name"])

    tokenizer = initialize_tokenizer(config_data["model_name"])

    embeddings = embedding_function()

    vectordb = Chroma(embedding_function=embeddings, persist_directory=config_data["persist_directory"])

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectordb.as_retriever()

    # build huggingface pipeline for using zephyr-7b-beta
    llm_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            use_cache=True,
            device_map="auto",
            max_length=4096, # 4096
            do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
    )

    # specify the llm
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # Contextualize question
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # Answer question
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use five sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain