import logging

from langchain_core.retrievers import BaseRetriever

from src.ai_agent.states import RAGState
from src.ai_agent.utils import format_documents
from src.ai_agent.nodes.base import BaseNode


logger = logging.getLogger(__name__)


class RetrieverNode(BaseNode):
    def __init__(self, retriever: BaseRetriever) -> None:
        self._retriever = retriever

    async def execute(self, state: RAGState) -> dict:
        logger.info("---RETRIEVE---")
        messages = state["messages"]
        last_message = messages[-1]
        query = last_message.content
        documents = await self._retriever.ainvoke(query)
        return {"documents": format_documents(documents)}
