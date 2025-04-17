from datetime import datetime

from typing import Sequence, Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import MessageModel
from src.infrastructure.database.crud.base_crud import BaseCRUD


class MessageCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, message: MessageModel) -> int:
        self._session.add(message)
        id = message.id
        await self._session.commit()
        await self._session.refresh(message)
        return id

    async def read_by_chat_id(self, chat_id: str) -> Sequence[Optional[MessageModel]]:
        stmt = (
            select(MessageModel)
            .where(MessageModel.chat_id == chat_id)
        )
        messages = await self._session.execute(stmt)
        return messages.scalars().all()

    async def read_by_chat_id_with_limit(
            self,
            chat_id: str,
            page: int = 1,
            limit: int = 5
    ) -> Sequence[Optional[MessageModel]]:
        offset = (page - 1) * limit
        stmt = (
            select(MessageModel)
            .where(MessageModel.chat_id == chat_id)
            .offset(offset)
            .limit(limit)
        )
        messages = await self._session.execute(stmt)
        return messages.scalars().all()

    async def read_all(self) -> Sequence[Optional[MessageModel]]:
        stmt = select(MessageModel)
        messages = await self._session.execute(stmt)
        return messages.scalars().all()

    async def read_all_with_limit(
            self,
            page: int = 1,
            limit: int = 5
    ) -> Sequence[Optional[MessageModel]]:
        offset = (page - 1) * limit
        stmt = (
            select(MessageModel)
            .offset(offset)
            .limit(limit)
        )
        messages = await self._session.execute(stmt)
        return messages.scalars().all()

    async def read_count(self) -> Optional[int]:
        stmt = (
            select(func.count)
            .select_from(MessageModel)
        )
        messages_count = await self._session.execute(stmt)
        return messages_count.scalar_one_or_none()

    async def read_count_by_chat_id(self, chat_id: str) -> Optional[int]:
        stmt = (
            select(func.count)
            .select_from(MessageModel)
            .where(MessageModel.chat_id == chat_id)
        )
        messages_count = await self._session.execute(stmt)
        return messages_count.scalar_one_or_none()

    async def read_count_per_day(self) -> Sequence[Tuple[datetime, int]]:
        stmt = (
            select(
                func.date(MessageModel.created_at).label("date"),
                func.count().label("count")
            )
            .group_by(func.date(MessageModel.created_at))
            .order_by(func.date(MessageModel.created_at))
        )
        counts_per_days = await self._session.execute(stmt)
        return counts_per_days.scalars().all()
