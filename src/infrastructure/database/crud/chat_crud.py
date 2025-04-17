from datetime import datetime

from typing import Sequence, Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import ChatModel
from src.infrastructure.database.crud.base_crud import BaseCRUD


class ChatCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, chat: ChatModel) -> int:
        self._session.add(chat)
        id = chat.id
        await self._session.commit()
        await self._session.refresh(chat)
        return id

    async def read_by_chat_id(self, chat_id: str) -> Optional[ChatModel]:
        stmt = (
            select(ChatModel)
            .where(ChatModel.chat_id == chat_id)
        )
        chat = await self._session.execute(stmt)
        return chat.scalar_one_or_none()

    async def read_count(self) -> Optional[int]:
        stmt = (
            select(func.count)
            .select_from(ChatModel)
        )
        chats_count = await self._session.execute(stmt)
        return chats_count.scalar_one_or_none()

    async def read_count_per_day(self) -> Sequence[Tuple[datetime, int]]:
        stmt = (
            select(
                func.date(ChatModel.created_at).label("date"),
                func.count().label("count")
            )
            .group_by(func.date(ChatModel.created_at))
            .order_by(func.date(ChatModel.created_at))
        )
        count_per_days = await self._session.execute(stmt)
        return count_per_days.scalars().all()
