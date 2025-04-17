from typing import List, Optional, Union

from src.repository.base_repository import BaseRepository
from src.core.entities import UserMessage, AssistantMessage
from src.infrastructure.database.crud import MessageCRUD
from src.infrastructure.database.models import MessageModel
from src.mappers import MessageMapper


class MessageRepository(BaseRepository):
    def __init__(self, crud: MessageCRUD) -> None:
        self._crud = crud

    async def save(self, message: Union[UserMessage, AssistantMessage]) -> int:
        id = await self._crud.create(MessageModel(**message.model_dump()))
        return id

    async def get_by_chat_id(self, chat_id: str) -> List[Optional[Union[UserMessage, AssistantMessage]]]:
        messages = await self._crud.read_by_chat_id(chat_id)
        return [MessageMapper.from_orm(message) for message in messages] if messages else []
