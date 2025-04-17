from typing import List

from src.core.entities import Chat
from src.infrastructure.database.crud import ChatCRUD
from src.repository.base_repository import BaseRepository
from src.mappers import ChatMapper
from src.dto import PerDayCount


class ChatRepository(BaseRepository):
    def __init__(self, crud: ChatCRUD) -> None:
        self._crud = crud

    async def save(self, chat: Chat) -> int:
        return await self._crud.create(ChatMapper.to_orm(chat))

    async def get_by_chat_id(self, chat_id: str) -> Chat:
        chat = await self._crud.read_by_chat_id(chat_id)
        return ChatMapper.from_orm(chat)

    async def total_count(self) -> int:
        return await self._crud.read_count()

    async def count_per_day(self) -> List[PerDayCount]:
        ...
