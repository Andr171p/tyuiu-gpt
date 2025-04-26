import logging

from faststream.rabbit import RabbitRouter
from dishka.integrations.base import FromDishka

from src.core.use_cases import ChatAssistant
from src.core.domain import UserMessage, AssistantMessage


logger = logging.getLogger(__name__)


chat_router = RabbitRouter()


@chat_router.subscriber("chat.user-messages")
@chat_router.publisher("chat.assistant-messages")
async def answer(
        user_message: UserMessage,
        chat_assistant: FromDishka[ChatAssistant]
) -> AssistantMessage:
    logger.info("Received user message %s", user_message)
    return await chat_assistant.answer(user_message)
