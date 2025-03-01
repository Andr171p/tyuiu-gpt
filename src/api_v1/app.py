import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api_v1.routers import chat_router


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI()
    app.include_router(chat_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
