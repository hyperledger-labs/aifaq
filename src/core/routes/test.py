from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid


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


conversation = {}


def generate_unique_id():
    return str(uuid.uuid4())


responses = {
    "What is Hyperledger Fabric?": "Hyperledger Fabric is an open-source blockchain framework designed for enterprise solutions. It allows for a modular architecture where different components like consensus mechanisms, membership services, and ledger storage can be tailored to specific needs.",
    "How to install Hyperledger Fabric?": "**To install Hyperledger Fabric, follow these steps:** \n - Install Docker and Docker Compose.\n - Download the Hyperledger Fabric binaries and Docker images using the Fabric CA and Fabric binaries script.\n - Set up the environment variables for Fabric binaries.\n - Verify the installation by running Fabric sample network scripts.",
    "How to deploy a Hyperledger Fabric network?": "**To deploy a Hyperledger Fabric network:** \n - Define the network topology and configuration files (e.g., 'configtx.yaml').\n - Use the 'fabric-cli' or scripts to create channel artifacts.\n - Launch the network by starting the necessary Docker containers and services using 'docker-compose' or Kubernetes.\n - Instantiate and upgrade chaincode as needed.",
    "How to run a Hyperledger Fabric network?": "To run a Hyperledger Fabric network:\n1. Start the network by running 'docker-compose up' or the appropriate command for your setup.\n2. Use the Fabric CLI tools or SDKs to interact with the network, including creating and joining channels, and submitting transactions.\n3. Monitor the network's health and performance using Fabric's built-in tools or external monitoring solutions.",
    "How to ensure data privacy in Hyperledger Fabric?": "To ensure data privacy in Hyperledger Fabric:\n1. Use private data collections to restrict access to sensitive data.\n2. Implement access control policies and endorsement policies.\n3. Utilize encryption for data at rest and in transit.\n4. Regularly review and update security configurations and practices.",
}


def get_hyperledger_fabric_answer(question):
    return responses.get(question, "Question not found in the database.")


@router.get("/response-keys", response_model=List[Dict[str, str]])
def get_response_keys() -> List[Dict[str, str]]:
    # Create a list of dictionaries with 'id' and 'name' keys
    res = []
    for index, key in enumerate(responses.keys()):
        res.append({"id": str(index + 1), "name": key})

    return res


# TODO: Get all chats for a user in a paginated format
@router.post("/conversations")
def get_conversations(
    offset: int = 0, limit: int = 30, order: str = "updated"
) -> ResponseConversation:
    pass


# TODO: Get a single chat for a user
@router.post("/conversation/{id}")
def post_conversation(id: str):
    temp_conversation = conversation.get(id)
    if not temp_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return temp_conversation


@router.post("/conversation", response_model=ResponseConversation)
def post_conversation(item: RequestConversation) -> ResponseConversation:
    conversation_id = generate_unique_id()  # it will contain the id

    new_conversation = ResponseConversation(
        id=item.id,
        message=ResponseMessage(
            content=get_hyperledger_fabric_answer(item.content),
            type=1,
            id=str(uuid.uuid4()),
        ),
    )
    conversation[conversation_id] = new_conversation
    return new_conversation
