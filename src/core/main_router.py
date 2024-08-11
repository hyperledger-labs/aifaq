from fastapi import APIRouter

main_router = APIRouter()

# reply to GET requests, if the service is running
@main_router.get("/")
def hello():
    return {"msg": "hello"}