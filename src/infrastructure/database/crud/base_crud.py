from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import ModelType


class BaseCRUD(ABC):
    _session: "AsyncSession"

    @abstractmethod
    async def create(self, model: ModelType) -> int:
        raise NotImplemented
