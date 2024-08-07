import os
import uvicorn
from utils import load_yaml_file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes.main import router as main_router
from routes.test import router as test_router

config_data = load_yaml_file("config.yaml")

def create_app() -> FastAPI:
    # Create the FastAPI application
    app = FastAPI()

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # app.include_router(main_router)
    app.include_router(test_router)

    return app

uvicorn.run(create_app,host=config_data["host"],port=config_data["port"])