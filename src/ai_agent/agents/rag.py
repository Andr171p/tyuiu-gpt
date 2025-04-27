import logging

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.core.interfaces import AIAgent

from src.ai_agent.states import RAGState
from src.ai_agent.nodes import RetrieverNode, GenerationNode


logger = logging.getLogger(__name__)


class RAGAgent(AIAgent):
    def __init__(
            self,
            retriever_node: RetrieverNode,
            generation_node: GenerationNode,
            checkpoint_saver: BaseCheckpointSaver
    ) -> None:
        workflow = StateGraph(RAGState)
        workflow.add_node("retrieve", retriever_node)
        workflow.add_node("generate", generation_node)
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        self._graph = workflow.compile(checkpointer=checkpoint_saver)

    async def generate(self, thread_id: str, query: str) -> str:
        logger.info("RAG start generate with thread_id %s", thread_id)
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        output = await self._graph.ainvoke(inputs, config=config)
        logger.info("RAG finish generate with thread_id %s", thread_id)
        last_message = output["messages"][-1]
        return last_message.content
