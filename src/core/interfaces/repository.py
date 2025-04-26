from typing import List, Union
from abc import ABC, abstractmethod

from pydantic import BaseModel


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
