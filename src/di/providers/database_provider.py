from typing import AsyncIterable

from dishka import Provider, provide, Scope

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.database.db import create_session_maker
from src.infrastructure.database.crud import MessageCRUD
from src.repository import MessageRepository

from src.settings import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(settings.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_message_crud(self, session: AsyncSession) -> MessageCRUD:
        return MessageCRUD(session)

    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, crud: MessageCRUD) -> MessageRepository:
        return MessageRepository(crud)
