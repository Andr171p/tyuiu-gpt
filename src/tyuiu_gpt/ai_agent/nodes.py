from abc import ABC, abstractmethod

import logging

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from .states import RAGState
from .templates import GENERATION_TEMPLATE, SUMMARIZATION_TEMPLATE
from .utils import format_documents, create_llm_chain, format_messages


class BaseNode(ABC):
    @abstractmethod
    async def __call__(self, state: RAGState) -> dict: pass


class SummarizeNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(SUMMARIZATION_TEMPLATE, model)

    async def __call__(self, state: RAGState) -> dict[str, ...]:
        self.logger.info("---SUMMARIZE---")
        messages = state["messages"]
        formatted_messages = format_messages(messages)
        question = messages[-1].content
        summary = await self.llm_chain.ainvoke({
            "messages": formatted_messages,
            "question": question
        })
        question_with_summary = f"{summary}\n\n{question}"
        return {"question": question_with_summary}


class RetrieveNode(BaseNode):
    def __init__(self, retriever: BaseRetriever) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.retriever = retriever

    async def __call__(self, state: RAGState) -> dict[str, list[Document]]:
        self.logger.info("---RETRIEVE---")
        documents = await self.retriever.ainvoke(state["question"])
        return {"documents": documents}


class GenerateNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(GENERATION_TEMPLATE, model)

    async def __call__(self, state: RAGState) -> dict:
        self.logger.info("---GENERATE---")
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(state["documents"])
        })
        return {"messages": [message]}
