from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks

from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from faststream.rabbit import RabbitBroker

from src.tyuiu_gpt.base import AIAgent
from src.tyuiu_gpt.schemas import UserMessage
from src.tyuiu_gpt.infrastructure.websockets import BaseSocketManager


socket_chat_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Socket chat"],
    route_class=DishkaRoute
)


@socket_chat_router.websocket("/{chat_id}")
@inject
async def chat(
        websocket: WebSocket,
        chat_id: str,
        ai_agent: FromDishka[AIAgent],
        socket_manager: FromDishka[BaseSocketManager],
        background_tasks: BackgroundTasks,
        broker: FromDishka[RabbitBroker]
) -> None:
    await socket_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            user_message = UserMessage.model_validate(message)
            await socket_manager.send(chat_id, user_message)
            assistant_message = await ai_agent.generate(user_message)
            await socket_manager.send(chat_id, assistant_message)
            background_tasks.add_task(
                broker.publish,
                [user_message, assistant_message],
                queue="chat.tasks.messages"
            )
    except WebSocketDisconnect:
        await socket_manager.disconnect(chat_id)
