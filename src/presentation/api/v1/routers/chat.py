from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.core.use_cases import ChatAssistant
from src.core.entities import UserMessage, AssistantMessage, Chat


chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
    route_class=DishkaRoute
)


@chat_router.post(
    path="/completion",
    status_code=status.HTTP_200_OK,
    response_model=AssistantMessage
)
async def answer(
        user_message: UserMessage,
        chat_assistant: FromDishka[ChatAssistant]
) -> AssistantMessage:
    return await chat_assistant.answer(user_message)


@chat_router.get(
    path="/messages/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Chat
)
async def get_chat(chat_id: str) -> Chat:
    ...
