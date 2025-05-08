import os
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_mistralai.embeddings import MistralAIEmbeddings

def get_ragchain(filter):
    # Read config data
    config_data = load_yaml_file("config.yaml")

    load_dotenv(find_dotenv())

    api_key = os.getenv("MISTRALAI_API_KEY")

    # Define LLM
    model = ChatMistralAI(mistral_api_key=api_key, model=config_data["model_name"])

    # read prompt string from config file
    prompt_str = config_data["prompt"]

    # Check if FAISS directory exists
    if os.path.exists(config_data["persist_directory"]):
        try:
            # Define the embedding model
            embeddings = MistralAIEmbeddings(model=config_data["embedding_model"], mistral_api_key=api_key)
            
            # Load local vector db
            docsearch = FAISS.load_local(config_data["persist_directory"], embeddings, allow_dangerous_deserialization=True)

            # Define a retriever interface
            retriever = docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 5, "filter": filter})

            # Answer question with RAG
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
        except Exception as e:
            print(f"Error loading FAISS index: {e}. Falling back to LLM-only approach.")
            # Fall back to LLM-only approach

    # LLM-only approach (no RAG)
    direct_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_str),
            ("user", "{input}"),
        ]
    )
    
    # Create a simple chain that just passes input to the LLM
    direct_chain = direct_prompt | model
    
    # Wrap in a compatible interface
    class LLMOnlyChain:
        def __init__(self, chain):
            self.chain = chain
            
        def invoke(self, input_text):
            response = self.chain.invoke({"input": input_text})
            return {"answer": response.content}
    
    return LLMOnlyChain(direct_chain)