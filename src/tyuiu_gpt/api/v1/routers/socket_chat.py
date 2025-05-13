from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks

from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from faststream.rabbit import RabbitBroker

from src.tyuiu_gpt.interfaces import AIAgent
from src.tyuiu_gpt.schemas import UserMessage, AssistantMessage
from src.tyuiu_gpt.api.connection_managers import BaseConnectionManager


socket_chat_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Streaming chat"],
    route_class=DishkaRoute
)


@socket_chat_router.websocket("/{chat_id}")
@inject
async def chat(
        websocket: WebSocket,
        chat_id: str,
        ai_agent: FromDishka[AIAgent],
        connection_manager: FromDishka[BaseConnectionManager],
        background_tasks: BackgroundTasks,
        broker: FromDishka[RabbitBroker]
) -> None:
    await connection_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            user_message = UserMessage.model_validate(message)
            await connection_manager.send(chat_id, user_message)
            generated = await ai_agent.generate(user_message.chat_id, user_message.text)
            assistant_message = AssistantMessage(chat_id=user_message.chat_id, text=generated)
            await connection_manager.send(chat_id, assistant_message)
            background_tasks.add_task(
                broker.publish,
                [user_message, assistant_message],
                queue="chat.tasks.messages"
            )
    except WebSocketDisconnect:
        await connection_manager.disconnect(chat_id)
