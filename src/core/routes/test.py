from typing import List, AsyncGenerator
from fastapi import APIRouter
from pydantic import BaseModel
import uuid, asyncio
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


def get_hyperledger_fabric_answer(question):
    return responses.get(question, "Question not found in the database.")


def normalize_question(question: str) -> str:
    # Convert to lowercase and strip punctuation
    question = question.rstrip()
    return re.sub(r'[^\w\s]', '', question.lower())


async def conversation_stream(offset: int = 0, limit: int = 30, order: str = "updated") -> AsyncGenerator[ResponseConversation, None]:
    # Normalize the keys in the responses dictionary
    normalized_responses = {normalize_question(k): v for k, v in responses.items()}
    
    # Retrieve items based on offset and limit
    items = list(normalized_responses.items())[offset:offset + limit]
    
    for idx, (_, answer) in enumerate(items):
        conversation = ResponseConversation(
            id=str(uuid.uuid4()),
            message=ResponseMessage(
                content=answer,
                type=1,
                id=str(uuid.uuid4()),
            )
        )
        yield f"data: {conversation.json()}\n\n"
        await asyncio.sleep(0.1)  # Simulate processing time


@router.post("/conversations")
def get_conversations(
    offset: int = 0, limit: int = 30, order: str = "updated"
) -> ResponseConversation:
    return StreamingResponse(conversation_stream(offset, limit), media_type="application/json")


async def single_conversation_stream(question: str) -> AsyncGenerator[ResponseConversation, None]:
    question = normalize_question(question)
    answer = responses.get(question, "Question not found")

    conversation = ResponseConversation(
        id=str(uuid.uuid4()),
        message=ResponseMessage(
            content=answer,
            type=1,
            id=str(uuid.uuid4()),
        )
    )
    yield f"data: {conversation.json()}\n\n"
    await asyncio.sleep(0.1)  # Simulate processing time


@router.post("/conversation/{id}")
def post_conversation(id: str):
    return StreamingResponse(single_conversation_stream(id), media_type="application/json")


@router.post("/conversation", response_model=ResponseConversation)
def post_conversation(item: RequestConversation) -> ResponseConversation:
    return ResponseConversation(
        id=item.id,
        message=ResponseMessage(
            content=get_hyperledger_fabric_answer(item.content),
            type=1,
            id=str(uuid.uuid4()),
        ),
    )
