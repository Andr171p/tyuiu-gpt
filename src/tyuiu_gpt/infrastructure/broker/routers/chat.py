from faststream import Logger
from faststream.rabbit import RabbitRouter, RabbitBroker

from dishka.integrations.base import FromDishka

from src.tyuiu_gpt.service import ChatAssistant
from src.tyuiu_gpt.schemas import UserMessage, AssistantMessage


chat_router = RabbitRouter()


@chat_router.subscriber("chat.user-messages")
@chat_router.publisher("chat.assistant-messages")
async def answer(
        user_message: UserMessage,
        chat_assistant: FromDishka[ChatAssistant],
        broker: FromDishka[RabbitBroker],
        logger: Logger
) -> AssistantMessage:
    logger.info("Received user message %s", user_message)
    assistant_message = await chat_assistant.answer(user_message)
    await broker.publish([user_message, assistant_message], queue="chat.tasks.messages")
    return assistant_message
