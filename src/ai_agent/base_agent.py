from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    async def generate(self, *args) -> str:
        raise NotImplemented
