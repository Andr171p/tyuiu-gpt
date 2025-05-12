from abc import ABC, abstractmethod

from ..states import AgentState


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: AgentState) -> dict:
        raise NotImplemented

    async def __call__(self, state: AgentState) -> dict:
        return await self.execute(state)
