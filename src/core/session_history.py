import os
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_groq import ChatGroq

# We can Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# GROQ API key 
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Initializing our Groq LLM, we can change model as per need.
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# Dictionary to hold memory per session
store = {}

from langchain.memory import ConversationSummaryBufferMemory

def get_session_memory(session_id: str) -> ConversationSummaryBufferMemory:
    if session_id not in store:
        # Creating a chat history instance
        chat_history = ChatMessageHistory()

        # Create summary buffer memory using Groq LLM
        memory = ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit= 50,  # Adjust based on desired summary size
            memory_key="chat_history",
            return_messages=True,
            chat_memory=chat_history,
            verbose = True
        )

        store[session_id] = memory

    return store[session_id]
