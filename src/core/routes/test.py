from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix="/api/test"
)

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
    "What is Hyperledger Fabric?": "Hyperledger Fabric is an open-source blockchain framework designed for enterprise solutions. It allows for a modular architecture where different components like consensus mechanisms, membership services, and ledger storage can be tailored to specific needs.",
    "How to install Hyperledger Fabric?": "To install Hyperledger Fabric, follow these steps:\n1. Install Docker and Docker Compose.\n2. Download the Hyperledger Fabric binaries and docker images using the Fabric CA and Fabric binaries script.\n3. Set up the environment variables for Fabric binaries.\n4. Verify the installation by running Fabric sample network scripts.",
    "How to deploy a Hyperledger Fabric network?": "To deploy a Hyperledger Fabric network:\n1. Define the network topology and configuration files (e.g., 'configtx.yaml').\n2. Use the 'fabric-cli' or scripts to create channel artifacts.\n3. Launch the network by starting the necessary Docker containers and services using 'docker-compose' or Kubernetes.\n4. Instantiate and upgrade chaincode as needed.",
    "How to run a Hyperledger Fabric network?": "To run a Hyperledger Fabric network:\n1. Start the network by running 'docker-compose up' or the appropriate command for your setup.\n2. Use the Fabric CLI tools or SDKs to interact with the network, including creating and joining channels, and submitting transactions.\n3. Monitor the network's health and performance using Fabric's built-in tools or external monitoring solutions.",
    "How to ensure data privacy in Hyperledger Fabric?": "To ensure data privacy in Hyperledger Fabric:\n1. Use private data collections to restrict access to sensitive data.\n2. Implement access control policies and endorsement policies.\n3. Utilize encryption for data at rest and in transit.\n4. Regularly review and update security configurations and practices."
}

def get_hyperledger_fabric_answer(question):
    return responses.get(question, "Question not found in the database.")

# TODO: Get all chats for a user in a paginated format
@router.post("/conversations")
def get_conversations(offset: int = 0, limit: int = 30, order: str = "updated") -> ResponseConversation:
    pass

# TODO: Get a single chat for a user
@router.post("/conversation/{id}")
def post_conversation(id:str):
    pass

@router.post("/conversation", response_model=ResponseConversation)
def post_conversation(item: RequestConversation) -> ResponseConversation:
    return ResponseConversation(
        id=item.id,
        message=ResponseMessage(
            content=get_hyperledger_fabric_answer(item.content),
            type=1,
            id=str(uuid.uuid4())
        ),
    )