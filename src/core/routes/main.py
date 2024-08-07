from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conversation import get_conversation

conversational_rag_chain = get_conversation()

# define the Query class that contains the question
class Query(BaseModel):
    text: str

#Initialization of the router :
router = APIRouter()

# reply to POST requests: '{"text": "How to install Hyperledger fabric?"}' 
@router.post("/query")
def answer(q: Query):
    question = q.text
    ai_msg_1 = conversational_rag_chain.invoke(
        {"input": question}, 
        config={"configurable": {"session_id": "1"}}, 
        )["answer"]

    return {"msg": ai_msg_1}