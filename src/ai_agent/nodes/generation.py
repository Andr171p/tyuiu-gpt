from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from src.ai_agent.states import RAGState
from src.ai_agent.nodes.base import BaseNode


class GenerationNode(BaseNode):
    def __init__(self, prompt: ChatPromptTemplate, model: BaseChatModel) -> None:
        self._llm_chain = prompt | model | StrOutputParser()

    async def execute(self, state: RAGState) -> dict:
        messages = state["messages"]
        last_message = messages[-1]
        question = last_message.content
        documents = state["documents"]
        message = await self._llm_chain.ainvoke({"question": question, "context": documents})
        return {"messages": [message]}
