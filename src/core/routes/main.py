from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from conversation import initialize_models, generate_response
model, tokenizer, vectordb = initialize_models()
class Query(BaseModel):
    text: str


router = APIRouter()

@router.post("/query")
async def stream_answer(q: Query, request: Request):
    question = q.text
    session_id = "1" 
    
    async def event_generator():
        try:
            for token in generate_response(session_id, model, tokenizer, question, vectordb):
                if await request.is_disconnected():
                    break
                yield {"data": token}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return EventSourceResponse(event_generator())
