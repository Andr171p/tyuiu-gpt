from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.settings import PostgresSettings


def create_session_maker(pg_settings: PostgresSettings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=pg_settings.url)
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )
