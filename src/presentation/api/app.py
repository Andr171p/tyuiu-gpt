import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from src.presentation.api.lifespan import lifespan
from src.presentation.api.v1.routers import (
    chat_router,
    socket_chat_router
)
from src.di import container


def create_fastapi_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI(lifespan=lifespan)
    app.include_router(chat_router)
    app.include_router(socket_chat_router)
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
