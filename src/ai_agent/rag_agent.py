import logging

from typing import Union

from langchain.prompts import ChatPromptTemplate

from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models.llms import LLM
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


from src.core.interfaces import BaseAIAgent
from src.ai_agent.utils import format_documents


logger = logging.getLogger(__name__)


class RAGAgent(BaseAIAgent):
    def __init__(
            self,
            retriever: BaseRetriever,
            prompt_template: str,
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._rag_chain = (
                {
                    "context": retriever | format_documents,
                    "question": RunnablePassthrough()
                } |
                ChatPromptTemplate.from_template(prompt_template) |
                model |
                StrOutputParser()
        )
        logger.info("Build RAG chain successfully")

    async def generate(self, thread_id: str, query: str) -> str:
        output = await self._rag_chain.ainvoke(query)
        return output
