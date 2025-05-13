from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, END, StateGraph, MessagesState

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel

from ..interfaces import AIAgent

from .states import AgentState
from .nodes import RetrieverNode, GenerationNode


class RAGAgent(AIAgent):
    def __init__(
            self,
            retriever: RetrieverNode,
            generation: GenerationNode,
            checkpoint_saver: BaseCheckpointSaver
    ) -> None:
        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve", retriever)
        workflow.add_node("generate", generation)

        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        self.graph = workflow.compile(checkpointer=checkpoint_saver)

    async def generate(self, thread_id: str, query: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        outputs = await self.graph.ainvoke(inputs, config=config)
        last_message = outputs["messages"][-1]
        return last_message.content


class ReACTAgent(AIAgent):
    def __init__(
            self,
            checkpoint_saver: BaseCheckpointSaver,
            tools: list[BaseTool],
            prompt_template: str,
            model: BaseChatModel
    ) -> None:
        workflow = StateGraph(MessagesState)
        agent = create_react_agent(
            tools=tools,
            state_modifier=prompt_template,
            model=model
        )
        workflow.add_node("agent", agent)
        workflow.add_edge(START, "agent")
        self.graph = workflow.compile(checkpointer=checkpoint_saver)

    async def generate(self, thread_id: str, query: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        output = await self.graph.ainvoke(inputs, config=config)
        last_message = output.get("messages")[-1]
        return last_message.content

