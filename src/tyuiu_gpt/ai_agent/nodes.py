import logging

from abc import ABC, abstractmethod

from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from .states import AgentState
from .utils import format_documents
from .templates import GENERATION_TEMPLATE


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: AgentState) -> dict:
        raise NotImplemented

    async def __call__(self, state: AgentState) -> dict:
        return await self.execute(state)


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


class GenerationNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = (
            ChatPromptTemplate.from_template(GENERATION_TEMPLATE)
            | model
            | StrOutputParser()
        )

    async def execute(self, state: AgentState) -> dict:
        self.logger.info("---GENERATION---")
        messages = state["messages"]
        last_message = messages[-1]
        question = last_message.content
        context = state["context"]
        message = await self.llm_chain.ainvoke({"question": question, "context": context})
        return {"messages": [message]}
