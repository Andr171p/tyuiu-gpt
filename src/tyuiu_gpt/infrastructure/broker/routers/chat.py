from faststream import Logger
from faststream.rabbit import RabbitRouter, RabbitBroker

from dishka.integrations.base import FromDishka

from src.tyuiu_gpt.interfaces import AIAgent
from src.tyuiu_gpt.schemas import UserMessage, AssistantMessage


chat_router = RabbitRouter()


@chat_router.subscriber("chat.user-messages")
@chat_router.publisher("chat.assistant-messages")
async def answer(
        user_message: UserMessage,
        ai_agent: FromDishka[AIAgent],
        broker: FromDishka[RabbitBroker],
        logger: Logger
) -> AssistantMessage:
    logger.info("Received user message %s", user_message)
    generated = await ai_agent.generate(user_message.chat_id, user_message.text)
    assistant_message = AssistantMessage(chat_id=user_message.chat_id, text=generated)
    await broker.publish([user_message, assistant_message], queue="chat.tasks.messages")
    return assistant_message
