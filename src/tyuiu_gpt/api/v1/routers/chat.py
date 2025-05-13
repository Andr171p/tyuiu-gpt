from fastapi import APIRouter, status, Query, BackgroundTasks

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from faststream.rabbit import RabbitBroker

from src.tyuiu_gpt.interfaces import AIAgent, MessageRepository
from src.tyuiu_gpt.schemas import UserMessage, AssistantMessage, ChatPage
from src.tyuiu_gpt.constants import DEFAULT_PAGE, DEFAULT_LIMIT, MIN_PAGE, MIN_LIMIT


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
        ai_agent: FromDishka[AIAgent],
        background_tasks: BackgroundTasks,
        broker: FromDishka[RabbitBroker]
) -> AssistantMessage:
    generated = await ai_agent.generate(user_message.chat_id, user_message.text)
    assistant_message = AssistantMessage(chat_id=user_message.chat_id, text=generated)
    background_tasks.add_task(
        broker.publish,
        [user_message, assistant_message],
        queue="chat.tasks.messages"
    )
    return assistant_message


@chat_router.get(
    path="/messages/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChatPage
)
async def get_chat(
        chat_id: str,
        message_repository: FromDishka[MessageRepository],
        page: int = Query(ge=MIN_PAGE, default=DEFAULT_PAGE),
        limit: int = Query(ge=MIN_LIMIT, default=DEFAULT_LIMIT)
) -> ChatPage:
    total = await message_repository.count()
    messages = await message_repository.paginate(chat_id, page, limit)
    return ChatPage(
            total=total,
            page=page,
            limit=limit,
            chat_id=chat_id,
            messages=messages
        )
