from typing import List

from src.core.entities import Chat, ChatPage, BaseMessage, MessagesDateToCount
from src.repository import MessageRepository


class ChatHistoryManager:
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    async def save_messages(self, messages: List[BaseMessage]) -> None:
        await self._message_repository.save_many(messages)

    async def chat_history(self, chat_id: str) -> Chat:
        messages = await self._message_repository.get_by_chat_id(chat_id)
        return Chat(chat_id=chat_id, messages=messages)

    async def chat_history_page(self, chat_id: str, page: int = 1, limit: int = 10) -> ChatPage:
        total = await self._message_repository.total_count()
        messages = await self._message_repository.get_by_chat_id_with_limit(chat_id, page, limit)
        return ChatPage(
            chat_id=chat_id,
            page=page,
            limit=limit,
            total=total,
            messages=messages
        )

    async def chat_length(self, chat_id: str) -> int:
        return await self._message_repository.get_count_by_chat_id(chat_id)

    async def messages_date_to_count(self) -> MessagesDateToCount:
        date_to_count = await self._message_repository.count_per_day()
        return MessagesDateToCount(distribution=date_to_count)
