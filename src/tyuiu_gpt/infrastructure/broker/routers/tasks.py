from faststream import Logger
from faststream.rabbit import RabbitRouter

from dishka.integrations.base import FromDishka

from src.tyuiu_gpt.schemas import BaseMessage
from src.tyuiu_gpt.interfaces import MessageRepository


tasks_router = RabbitRouter()


@tasks_router.subscriber("chat.tasks.messages")
async def save_messages(
        messages: list[BaseMessage],
        repository: FromDishka[MessageRepository],
        logger: Logger
) -> None:
    await repository.bulk_create(messages)
    logger.info("Messages saved successfully")
