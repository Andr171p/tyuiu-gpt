import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from src.presentation.api.v1.routers import chatbot_router
from src.presentation.di import container


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI()
    app.include_router(chatbot_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_dishka(
        container=container,
        app=app,
    )
    return app
