import os
import locale
import subprocess
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)
import gradio as gr
from langchain.llms import HuggingFacePipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_text_splitters import MarkdownHeaderTextSplitter

# LCEL related imports
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.schema.output_parser import StrOutputParser
# from langchain.prompts import ChatPromptTemplate

# fixing unicode error in google colab
locale.getpreferredencoding = lambda: "UTF-8"

############################################
# Functions
############################################


# Function to load a 4-bit quantized model
def load_quantized_model(model_name: str):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.bfloat16, quantization_config=bnb_config
    )
    return model


# Function to initialize tokenizer
def initialize_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.bos_token_id = 1
    return tokenizer


# Function to clone a repository
def clone_repo(repo_name, target_dir):
    repo_url = f"https://github.com/{repo_name}.git"
    try:
        subprocess.check_output(["git", "clone", repo_url, target_dir])
        print(f"Success! Repository {repo_name} cloned into {target_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Fail... {str(e)}")
        return False


# Function to get a list of files with specific extensions
def get_file_list(target_dir, ext_whitelist):
    filtered_files = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if any(file.endswith(ext) for ext in ext_whitelist):
                filtered_files.append(os.path.join(root, file))
    return filtered_files


# Function to create documents from files
def create_documents(files):
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=6000, chunk_overlap=600)
    documents = []
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            text = file.read()
        md_splits = markdown_splitter.split_text(text)
        docs = text_splitter.split_documents(md_splits)
        documents.extend(docs)
    return documents


# Function to create a retriever
def create_retriever(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cuda"},
    )
    vectordb = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory="chroma_db"
    )
    return vectordb.as_retriever()


# Define the conversation function
def create_conversation(query: str, chat_history: list) -> tuple:
    try:
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=False
        )
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=retriever, memory=memory, get_chat_history=lambda h: h
        )
        result = qa_chain({"question": query, "chat_history": chat_history})
        chat_history.append((query, result["answer"]))
        return "", chat_history
    except Exception as e:
        chat_history.append((query, str(e)))
        return "", chat_history


############################################
# Setup model
############################################

# Load model and initialize tokenizer
model_name = "anakin87/zephyr-7b-alpha-sharded"
model = load_quantized_model(model_name)
tokenizer = initialize_tokenizer(model_name)

# Configure pipeline
my_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    use_cache=True,
    device_map="auto",
    max_length=2048,
    do_sample=True,
    top_k=5,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)

# Specify the LLM and prepare documents and retriever
llm = HuggingFacePipeline(pipeline=my_pipeline)

############################################
# Set repository and file extensions
############################################

repo_name = "hyperledger/iroha"
ext_whitelist = [".md", ".rst"]

############################################
# Clone repo, filter files, create documents and retreiver"""
############################################

target_dir = repo_name.split("/")[-1]

clone_repo(repo_name, target_dir)
files = get_file_list(target_dir, ext_whitelist)
documents = create_documents(files)
retriever = create_retriever(documents)

### Langchain LCEL implementation - but no memory!

# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
# chain.invoke("How do I restart an Iroha node?")

############################################
# Run Gradio"""
############################################

# Build Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat with your data (Zephyr 7B Alpha)")
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(create_conversation, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)
