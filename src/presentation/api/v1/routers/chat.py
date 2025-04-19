from typing import Union

from fastapi import APIRouter, status, Query, BackgroundTasks
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from faststream.rabbit import RabbitBroker

from src.core.use_cases import ChatAssistant
from src.core.entities import UserMessage, AssistantMessage
from src.repository import MessageRepository
from src.presentation.api.v1.schemas import ChatSchema, ChatPageSchema


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
        chat_assistant: FromDishka[ChatAssistant],
        background_tasks: BackgroundTasks,
        broker: FromDishka[RabbitBroker]
) -> AssistantMessage:
    assistant_message = await chat_assistant.answer(user_message)
    background_tasks.add_task(
        broker.publish,
        [user_message, assistant_message],
        queue="chat.tasks.messages"
    )
    return assistant_message


@chat_router.get(
    path="/messages/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Union[ChatSchema, ChatPageSchema]
)
async def get_chat(
        chat_id: str,
        repository: FromDishka[MessageRepository],
        is_paginated: bool = Query(default=False),
        page: int = Query(ge=1, default=1),
        limit: int = Query(ge=1, default=10)
) -> Union[ChatSchema, ChatPageSchema]:
    if is_paginated:
        messages = await repository.list_page(chat_id, page, limit)
        total = await repository.total_count()
        return ChatPageSchema(
            total=total,
            page=page,
            limit=limit,
            chat_id=chat_id,
            messages=messages
        )
    messages = await repository.get(chat_id)
    return ChatSchema(chat_id=chat_id, messages=messages)
