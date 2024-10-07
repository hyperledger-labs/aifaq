from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from conversation import initialize_models, generate_response

model, tokenizer, vectordb = initialize_models()

router = APIRouter()

class ResponseMessage(BaseModel):
    content: str
    type: int
    id: str

class RequestQuery(BaseModel):
    id: str
    content: str

class ResponseQuery(BaseModel):
    id: str
    message: ResponseMessage

@router.post("/query", response_model=ResponseQuery)
async def answer_query(item: RequestQuery) -> ResponseQuery:
    try:
        response = generate_response("1", model, tokenizer, item.content, vectordb)
        return ResponseQuery(
            id=item.id,
            message=ResponseMessage(
                content=response,
                type=1,
                id=str(uuid.uuid4()),
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
