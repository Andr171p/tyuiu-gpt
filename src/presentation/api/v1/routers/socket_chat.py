from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from src.core.entities import UserMessage
from src.core.use_cases import ChatAssistant
from src.presentation.api.connection_managers import BaseConnectionManager


socket_chat_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Stream chat with AI assistant"],
    route_class=DishkaRoute
)


@socket_chat_router.websocket("/{chat_id}")
@inject
async def chat(
        websocket: WebSocket,
        chat_id: str,
        chat_assistant: FromDishka[ChatAssistant],
        connection_manager: FromDishka[BaseConnectionManager]
) -> None:
    await connection_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            user_message = UserMessage.model_validate(message)
            await connection_manager.send(chat_id, user_message)
            assistant_message = await chat_assistant.answer(user_message)
            await connection_manager.send(chat_id, assistant_message)
    except WebSocketDisconnect:
        await connection_manager.disconnect(chat_id)
