from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.core.interfaces import AIAgent

from ..states import AgentState
from ..nodes import RetrieverNode, GenerationNode


class RAGAgent(AIAgent):
    def __init__(
            self,
            retriever_node: RetrieverNode,
            generation_node: GenerationNode,
            checkpoint_saver: BaseCheckpointSaver
    ) -> None:
        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve", retriever_node)
        workflow.add_node("generate", generation_node)

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
