from abc import ABC, abstractmethod


class BaseAIAgent(ABC):
    @abstractmethod
    async def generate(self, *args) -> str:
        raise NotImplemented
