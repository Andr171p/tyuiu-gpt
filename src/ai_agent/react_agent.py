import logging

from typing import List

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, StateGraph, MessagesState

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel

from src.core.interfaces import BaseAIAgent


logger = logging.getLogger(__name__)


class ReACTAgent(BaseAIAgent):
    def __init__(
            self,
            checkpoint_saver: BaseCheckpointSaver,
            tools: List[BaseTool],
            prompt_template: str,
            model: BaseChatModel
    ) -> None:
        agent = create_react_agent(
            tools=tools,
            state_modifier=prompt_template,
            model=model
        )
        graph = StateGraph(MessagesState)
        graph.add_node("agent", agent)
        graph.add_edge(START, "agent")
        self._compiled_graph = graph.compile(checkpointer=checkpoint_saver)
        logger.info("Graph compiled successfully")

    async def generate(self, thread_id: str, query: str) -> str:
        logger.info("Start generate for %s", thread_id)
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        output = await self._compiled_graph.ainvoke(inputs, config=config)
        last_message = output.get("messages")[-1]
        return last_message.content
