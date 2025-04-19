import logging

from typing import List

from faststream.rabbit import RabbitRouter
from dishka.integrations.base import FromDishka

from src.core.entities import BaseMessage
from src.repository import MessageRepository


logger = logging.getLogger(__name__)


tasks_router = RabbitRouter()


@tasks_router.subscriber("chat.tasks.save-messages")
async def save_messages(
        messages: List[BaseMessage],
        repository: FromDishka[MessageRepository]
) -> None:
    await repository.save_many(messages)
    logger.info("Messages saves successfully")
