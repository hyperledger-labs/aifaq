from utils import load_yaml_file
from main import get_conversation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

config_data = load_yaml_file("config.yaml")

conversational_rag_chain = get_conversation()

# define the Query class that contains the question
class Query(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# reply to GET requests, if the service is running
@app.get("/")
def hello():
    return {"msg": "hello"}

# reply to POST requests: '{"text": "How to install Hyperledger fabric?"}' 
@app.post("/query")
def answer(q: Query):
    question = q.text
    ai_msg_1 = conversational_rag_chain.invoke(
        {"input": question}, 
        config={"configurable": {"session_id": "1"}}, 
        )["answer"]

    return {"msg": ai_msg_1}

# reply to CHAT requests from the front end
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    question = request.message
    ai_msg_1 = conversational_rag_chain.invoke(
        {"input": question}, 
        config={"configurable": {"session_id": "1"}}, 
        )["answer"]
    
    return ChatResponse(response=ai_msg_1)

uvicorn.run(app,host=config_data["host"],port=config_data["port"])