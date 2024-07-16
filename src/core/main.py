import torch
from utils import load_yaml_file
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from model import load_quantized_model
from tokenizer import initialize_tokenizer
from embeddings import embedding_function
from session_history import get_session_history


def get_ragchain():
    config_data = load_yaml_file("config.yaml")

    model = load_quantized_model(config_data["model_name"])

    #tokenizer_kwargs = {'truncation': True}
    tokenizer = initialize_tokenizer(config_data["model_name"])

    embeddings = embedding_function()

    vectordb = Chroma(embedding_function=embeddings, persist_directory=config_data["persist_directory"])

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectordb.as_retriever()

    # build huggingface pipeline for using zephyr-7b-beta
    llm_pipeline = pipeline(
            "text-generation",
            model=model,
            truncation=True,
            tokenizer=tokenizer,
            use_cache=True,
            device_map="auto",
            max_length=4096, # 4096
            do_sample=True,
            top_k=3,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
    )

    # specify the llm
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # Answer question
    qa_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
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
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain