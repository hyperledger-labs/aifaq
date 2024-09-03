from typing import List, AsyncGenerator
from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import asyncio
from fastapi.responses import StreamingResponse
import re

router = APIRouter(prefix="/api/test")


class ResponseMessage(BaseModel):
    id: str
    content: str
    type: int


class ResponseConversation(BaseModel):
    id: str
    message: ResponseMessage


class RequestConversation(BaseModel):
    id: str
    content: str
    type: int


responses = {
    "what is hyperledger fabric": "Hyperledger Fabric is an open-source blockchain framework designed for enterprise solutions. It allows for a modular architecture where different components like consensus mechanisms, membership services, and ledger storage can be tailored to specific needs.",
    "how to install hyperledger fabric": "To install Hyperledger Fabric, follow these steps:\n1. Install Docker and Docker Compose.\n2. Download the Hyperledger Fabric binaries and docker images using the Fabric CA and Fabric binaries script.\n3. Set up the environment variables for Fabric binaries.\n4. Verify the installation by running Fabric sample network scripts.",
    "how to deploy a hyperledger fabric network": "To deploy a Hyperledger Fabric network:\n1. Define the network topology and configuration files (e.g., 'configtx.yaml').\n2. Use the 'fabric-cli' or scripts to create channel artifacts.\n3. Launch the network by starting the necessary Docker containers and services using 'docker-compose' or Kubernetes.\n4. Instantiate and upgrade chaincode as needed.",
    "how to run a hyperledger fabric network": "To run a Hyperledger Fabric network:\n1. Start the network by running 'docker-compose up' or the appropriate command for your setup.\n2. Use the Fabric CLI tools or SDKs to interact with the network, including creating and joining channels, and submitting transactions.\n3. Monitor the network's health and performance using Fabric's built-in tools or external monitoring solutions.",
    "how to ensure data privacy in hyperledger fabric": "To ensure data privacy in Hyperledger Fabric:\n1. Use private data collections to restrict access to sensitive data.\n2. Implement access control policies and endorsement policies.\n3. Utilize encryption for data at rest and in transit.\n4. Regularly review and update security configurations and practices.",
}


def normalize_question(question: str) -> str:
    question = question.rstrip()
    return re.sub(r"[^\w\s]", "", question.lower())


def create_conversation_response(content: str) -> ResponseConversation:
    return ResponseConversation(
        id=str(uuid.uuid4()),
        message=ResponseMessage(
            content=content,
            type=1,
            id=str(uuid.uuid4()),
        ),
    )


@router.get("/conversations", response_model=List[ResponseConversation])
def get_conversations(
    offset: int = 0, limit: int = 30, order: str = "updated"
) -> List[ResponseConversation]:
    normalized_responses = {normalize_question(k): v for k, v in responses.items()}
    items = list(normalized_responses.items())[offset : offset + limit]

    return [create_conversation_response(answer) for _, answer in items]


@router.get("/conversation/{id}", response_model=ResponseConversation)
def get_single_conversation(id: str) -> ResponseConversation:
    question = normalize_question(id)
    answer = responses.get(question, "Question not found")

    return create_conversation_response(answer)


async def single_conversation_stream(question: str) -> AsyncGenerator[str, None]:
    question = normalize_question(question)
    answer = responses.get(question, "Question not found")

    conversation = create_conversation_response(answer)
    yield f"data: {conversation.json()}\n\n"
    await asyncio.sleep(0.1)


@router.post("/conversation")
async def post_conversation(item: RequestConversation) -> StreamingResponse:
    return StreamingResponse(
        single_conversation_stream(item.content), media_type="text/event-stream"
    )
