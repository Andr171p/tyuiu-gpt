import logging

from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.broker.app import create_faststream_app


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    faststream_app = await create_faststream_app()
    await faststream_app.broker.start()
    logger.info("Broker started")
    yield
    await faststream_app.broker.close()
    logger.info("Broker closed")
