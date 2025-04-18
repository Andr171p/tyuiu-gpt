from typing import Union

from fastapi import APIRouter, status, Query
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.core.use_cases import ChatAssistant, ChatHistoryManager
from src.core.entities import UserMessage, AssistantMessage, Chat, ChatPage


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
    response_model=Union[Chat, ChatPage]
)
async def get_chat(
        chat_id: str,
        chat_history_manager: FromDishka[ChatHistoryManager],
        is_paginated: bool = Query(default=False),
        page: int = Query(ge=1, default=1),
        limit: int = Query(ge=1, default=10)
) -> Union[Chat, ChatPage]:
    if is_paginated:
        return await chat_history_manager.chat_history_page(chat_id, page, limit)
    return await chat_history_manager.chat_history(chat_id)
