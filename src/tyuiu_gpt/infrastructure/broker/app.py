from faststream import FastStream
from faststream.rabbit import RabbitBroker

from dishka.integrations.faststream import setup_dishka

from .routers import chat_router, tasks_router
from src.tyuiu_gpt.ioc import container


async def create_faststream_app() -> FastStream:
    broker = await container.get(RabbitBroker)
    broker.include_routers(chat_router, tasks_router)
    app = FastStream(broker)
    setup_dishka(
        container=container,
        app=app,
        auto_inject=True
    )
    return app
