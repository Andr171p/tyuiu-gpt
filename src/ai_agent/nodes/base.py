from abc import ABC, abstractmethod

from src.ai_agent.states import RAGState


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: RAGState) -> dict:
        raise NotImplemented

    async def __call__(self, state: RAGState) -> dict:
        return await self.execute(state)
