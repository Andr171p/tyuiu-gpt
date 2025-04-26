from abc import ABC, abstractmethod


class AbstractAIAgent(ABC):
    @abstractmethod
    async def generate(self, *args) -> str:
        raise NotImplemented
