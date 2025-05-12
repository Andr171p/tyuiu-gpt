import logging

from langchain_core.retrievers import BaseRetriever

from .base import BaseNode
from ..states import AgentState
from ..utils import format_documents


class RetrieverNode(BaseNode):
    def __init__(self, retriever: BaseRetriever) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.retriever = retriever

    async def execute(self, state: AgentState) -> dict:
        self.logger.info("---RETRIEVE---")
        messages = state["messages"]
        last_message = messages[-1]
        query = last_message.content
        documents = await self.retriever.ainvoke(query)
        return {"context": format_documents(documents)}
