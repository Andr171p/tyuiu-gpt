from typing import Protocol

from .schemas import BaseMessage, UserMessage, AssistantMessage


class AIAgent(Protocol):
    async def generate(self, user_message: UserMessage) -> AssistantMessage: pass


class MessageRepository(Protocol):
    async def bulk_create(self, messages: list[BaseMessage]) -> None: pass

    async def read(self, chat_id: str) -> list[BaseMessage]: pass

    async def paginate(self, chat_id: str, page: int, limit: int) -> list[BaseMessage]: pass

    async def count(self) -> int: pass
