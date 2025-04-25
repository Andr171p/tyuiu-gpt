from typing import Any, Type, Optional

import logging

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.retrievers import BaseRetriever

from src.ai_agent.utils import format_documents


logger = logging.getLogger(__name__)


class RetrievalToolInput(BaseModel):
    query: str = Field(..., description="Вопрос пользователя")


class RetrievalTool(BaseTool):
    name: str = "RetrievalTool"
    description: str = """"
    Ищет информацию для ответы на вопросы абитуриента
    
    Может найти информация для ответа на вопросы касаемо:
    * процесса поступления
    * информация о направлениях подготовки
    * проходных / минимальных баллов
    * дополнительных баллов
    * льготы, квоты, особые права
    * прочие вопросы касаемо поступления
    """
    args_schema: Optional[Type[BaseModel]] = RetrievalToolInput

    def __init__(self, retriever: BaseRetriever, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._retriever = retriever

    def _run(self, query: str) -> str:
        logger.info("---RETRIEVE---")
        documents = self._retriever.invoke(query)
        return format_documents(documents)

    async def _arun(self, query: str) -> str:
        logger.info("---RETRIEVE---")
        documents = await self._retriever.ainvoke(query)
        return format_documents(documents)
