from utils import load_yaml_file
from main_router import main_router
from api_router import api_router 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

config_data = load_yaml_file("config.yaml")
    
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Include routers
app.include_router(main_router)
app.include_router(api_router, prefix="/api")

uvicorn.run(app,host=config_data["host"],port=config_data["port"])