from typing import Optional

import logging

from fastapi import WebSocket

from .base import BaseConnectionManager


class InMemoryConnectionManager(BaseConnectionManager):
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.logger.info("Created new active connection for %s", connection_id)

    async def disconnect(self, connection_id: str) -> None:
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            self.logger.info("Deleted connection for %s", connection_id)

    async def get_connection(self, connection_id: str) -> Optional[WebSocket]:
        return self.active_connections.get(connection_id)
