import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from .base import BaseNode
from ..states import AgentState


class GenerationNode(BaseNode):
    def __init__(self, prompt: ChatPromptTemplate, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = prompt | model | StrOutputParser()

    async def execute(self, state: AgentState) -> dict:
        self.logger.info("---GENERATION---")
        messages = state["messages"]
        last_message = messages[-1]
        question = last_message.content
        context = state["context"]
        message = await self.llm_chain.ainvoke({"question": question, "context": context})
        return {"messages": [message]}
