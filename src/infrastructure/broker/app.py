from faststream import FastStream
from dishka.integrations.faststream import setup_dishka

from src.infrastructure.broker.setup import create_broker
from src.infrastructure.broker.routers import chat_router, tasks_router

from src.di import container
from src.settings import RabbitSettings


def create_faststream_app() -> FastStream:
    broker = create_broker(RabbitSettings())
    broker.include_routers(chat_router, tasks_router)
    app = FastStream(broker)
    setup_dishka(
        container=container,
        app=app,
        auto_inject=True
    )
    return app
