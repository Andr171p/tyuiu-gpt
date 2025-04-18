from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from src.core.use_cases import ChatAssistant
from src.services.connection_managers import BaseConnectionManager


ws_chat_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Stream chat with AI assistant"],
    route_class=DishkaRoute
)


@ws_chat_router.websocket("/{chat_id}")
@inject
async def chat(
        websocket: WebSocket,
        chat_id: str,
        chat_assistant: FromDishka[ChatAssistant],
        connection_manager: FromDishka[BaseConnectionManager]
) -> ...:
    try:
        while True:
            ...
    except WebSocketDisconnect:
        ...

