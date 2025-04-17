import logging

from typing import List

from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, StateGraph, MessagesState

from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage
from langchain_core.language_models import BaseChatModel

from src.ai_agent.base_agent import BaseAgent


logger = logging.getLogger(__name__)


class ReACTAgent(BaseAgent):
    def __init__(
            self,
            checkpoint_saver: BaseCheckpointSaver,
            tools: List[BaseTool],
            prompt_template: str,
            model: BaseChatModel
    ) -> None:
        self._checkpoint_saver = checkpoint_saver
        self._tools = tools
        self._prompt_template = prompt_template
        self._model = model

    async def generate(self, thread_id: str, query: str) -> str:
        logger.info("Start generate response for %s", thread_id)
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        compiled_graph = self._build_and_compile_graph()
        response = await compiled_graph.ainvoke(inputs, config=config)
        message: BaseMessage = response.get("messages")[-1]
        return message.content

    def _build_and_compile_graph(self) -> CompiledStateGraph:
        react_agent = create_react_agent(
            tools=self._tools,
            state_modifier=self._prompt_template,
            model=self._model
        )
        graph = StateGraph(MessagesState)
        graph.add_node("agent", react_agent)
        graph.add_edge(START, "agent")
        return graph.compile(checkpointer=self._checkpoint_saver)
