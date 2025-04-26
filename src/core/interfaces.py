from typing import List, Union
from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.core.entities import BaseMessage


class AbstractAIAgent(ABC):
    @abstractmethod
    async def generate(self, *args) -> str:
        raise NotImplemented


class AbstractRepository(ABC):
    @abstractmethod
    async def save(self, model: BaseModel) -> int:
        raise NotImplemented

    @abstractmethod
    async def get(self, id: Union[str, int]) -> Union[BaseModel, List[BaseModel]]:
        raise NotImplemented

    @abstractmethod
    async def list(self) -> List[BaseModel]:
        raise NotImplemented


class AbstractMessageRepository(AbstractRepository):
    @abstractmethod
    async def save_many(self, messages: List[BaseMessage]) -> List[int]:
        raise NotImplemented

    @abstractmethod
    async def list_page(self, chat_id: str, page: int, limit: int) -> List[BaseMessage]:
        raise NotImplemented
