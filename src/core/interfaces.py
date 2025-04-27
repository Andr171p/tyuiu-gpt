from typing import (
    Protocol,
    Generic,
    TypeVar,
    List,
    Union,
    Optional
)
from abc import ABC, abstractmethod

from src.dto import CreationDateCount
from src.core.entities import BaseMessage


T = TypeVar("T")


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, thread_id: str, query: str) -> str:
        raise NotImplemented


class Repository(Protocol, Generic[T]):
    async def save(self, entity: T) -> int:
        raise NotImplemented

    async def get(self, id: Union[str, int]) -> Union[T, List[T]]:
        raise NotImplemented

    async def list(self) -> List[T]:
        raise NotImplemented


class MessageRepository(Repository[BaseMessage], Protocol):
    async def save_many(self, messages: List[BaseMessage]) -> List[int]:
        raise NotImplemented

    async def list_page(self, chat_id: str, page: int, limit: int) -> List[BaseMessage]:
        raise NotImplemented

    async def count_by_chat_id(self, chat_id: str) -> int:
        raise NotImplemented

    async def get_chat_ids(self) -> List[str]:
        raise NotImplemented

    async def count(self) -> int:
        raise NotImplemented

    async def count_by_creation_date(self) -> List[Optional[CreationDateCount]]:
        raise NotImplemented
