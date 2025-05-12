from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, StateGraph, MessagesState

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel

from src.core.interfaces import AIAgent


class ReACTAgent(AIAgent):
    def __init__(
            self,
            checkpoint_saver: BaseCheckpointSaver,
            tools: list[BaseTool],
            prompt_template: str,
            model: BaseChatModel
    ) -> None:
        agent = create_react_agent(
            tools=tools,
            state_modifier=prompt_template,
            model=model
        )
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", agent)
        workflow.add_edge(START, "agent")
        self.graph = workflow.compile(checkpointer=checkpoint_saver)

    async def generate(self, thread_id: str, query: str) -> str:

        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        output = await self.graph.ainvoke(inputs, config=config)
        last_message = output.get("messages")[-1]
        return last_message.content
