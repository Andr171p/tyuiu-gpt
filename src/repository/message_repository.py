from typing import List, Optional, Union

from src.repository.base_repository import BaseRepository
from src.core.entities import UserMessage, AssistantMessage, ChatPage
from src.infrastructure.database.crud import MessageCRUD
from src.infrastructure.database.models import MessageModel
from src.mappers import MessageMapper
from src.dto import PerDayCount


class MessageRepository(BaseRepository):
    def __init__(self, crud: MessageCRUD) -> None:
        self._crud = crud

    async def save(self, message: Union[UserMessage, AssistantMessage]) -> int:
        return await self._crud.create(MessageModel(**message.model_dump()))

    async def save_many(self, messages: List[Union[UserMessage, AssistantMessage]]) -> List[int]:
        return await self._crud.create_many([MessageModel(**message.model_dump()) for message in messages])

    async def get_by_chat_id(self, chat_id: str) -> List[Optional[Union[UserMessage, AssistantMessage]]]:
        messages = await self._crud.read_by_chat_id(chat_id)
        return [MessageMapper.from_orm(message) for message in messages] if messages else []

    async def get_page_by_chat_id(
            self,
            chat_id: str,
            page: int = 1,
            limit: int = 5
    ) -> ChatPage:
        messages = await self._crud.read_by_chat_id_with_limit(chat_id, page, limit)
        return ChatPage(
            chat_id=chat_id,
            page=page,
            limit=limit,
            total=await self.total_count(),
            messages=[MessageMapper.from_orm(message) for message in messages]
        )

    async def total_count(self) -> int:
        return await self._crud.read_count()

    async def count_per_day(self) -> List[Optional[PerDayCount]]:
        count_per_day = await self._crud.read_count_per_day()
        return [
            PerDayCount(date=date, count=count)
            for date, count in count_per_day
        ] if count_per_day else []
