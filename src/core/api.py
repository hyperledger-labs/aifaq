from utils import load_yaml_file
from main import get_ragchain
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

config_data = load_yaml_file("config.yaml")

rag_chain = get_ragchain()

# define the Query class that contains the question
class Query(BaseModel):
    text: str

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# it replies to GET requests, if the service is running
@app.get("/")
def hello():
    return {"msg": "hello"}

# reply to POST requests: '{"text": "How to install Hyperledger fabric?"}'
@app.post("/query")
def answer(q: Query):
    question = q.text
    result = rag_chain.invoke({"input": question})

    return {"msg": result}

uvicorn.run(app,host=config_data["host"],port=config_data["port"])