from typing import List, Optional

from src.core.entities import BaseMessage
from src.core.interfaces import MessageRepository
from src.dto import CreationDateCount, MessageMapper
from src.infrastructure.database.crud import MessageCRUD
from src.infrastructure.database.models import MessageModel


class MessageRepositoryImpl(MessageRepository):
    def __init__(self, crud: MessageCRUD) -> None:
        self._crud = crud

    async def save(self, message: BaseMessage) -> int:
        return await self._crud.create(MessageModel(**message.model_dump()))

    async def save_many(self, messages: List[BaseMessage]) -> List[int]:
        return await self._crud.create_many([MessageModel(**message.model_dump()) for message in messages])

    async def get(self, chat_id: str) -> List[Optional[BaseMessage]]:
        messages = await self._crud.read_by_chat_id(chat_id)
        return [MessageMapper.from_orm(message) for message in messages] if messages else []

    async def list(self) -> List[BaseMessage]:
        messages = await self._crud.read_all()
        return [MessageMapper.from_orm(message) for message in messages]

    async def list_page(
            self,
            chat_id: str,
            page: int = 1,
            limit: int = 5
    ) -> List[Optional[BaseMessage]]:
        messages = await self._crud.read_by_chat_id_with_limit(chat_id, page, limit)
        return [MessageMapper.from_orm(message) for message in messages] if messages else []

    async def count_by_chat_id(self, chat_id: str) -> int:
        return await self._crud.read_count_by_chat_id(chat_id)

    async def get_chat_ids(self) -> List[str]:
        chat_ids = await self._crud.read_unique_chat_ids()
        return [chat_id for chat_id in chat_ids]

    async def count(self) -> int:
        return await self._crud.read_total_count()

    async def count_by_creation_date(self) -> List[Optional[CreationDateCount]]:
        counts = await self._crud.read_count_per_day()
        return [
            CreationDateCount(date=date, count=count)
            for date, count in counts
        ] if counts else []
