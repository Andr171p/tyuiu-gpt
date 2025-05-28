from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import MessageModel
from src.tyuiu_gpt.schemas import BaseMessage
from src.tyuiu_gpt.base import MessageRepository


class SQLMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def bulk_create(self, messages: list[BaseMessage]) -> None:
        try:
            message_models = [MessageModel(**message.model_dump()) for message in messages]
            self.session.add_all(message_models)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Error while bulk creating messages: {e}")

    async def read(self, chat_id: str) -> list[BaseMessage]:
        try:
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
            )
            results = await self.session.execute(stmt)
            messages = results.scalars().all()
            return [BaseMessage.model_validate(message) for message in messages]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Error while reading messages: {e}")

    async def paginate(self, chat_id: str, page: int, limit: int) -> list[BaseMessage]:
        try:
            offset = (page - 1) * limit
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
                .offset(offset)
                .limit(limit)
            )
            results = await self.session.execute(stmt)
            messages = results.scalars().all()
            return [BaseMessage.model_validate(message) for message in messages]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Error while paginating messages: {e}")

    async def count(self) -> int:
        try:
            stmt = (
                select(func.count())
                .select_from(MessageModel)
            )
            count = await self.session.execute(stmt)
            return count.scalar()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Error while reading count messages: {e}")
