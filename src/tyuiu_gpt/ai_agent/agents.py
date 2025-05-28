from langgraph.graph.graph import CompiledGraph
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from ..base import AIAgent
from ..schemas import UserMessage, AssistantMessage

from .states import RAGState
from .nodes import SummarizeNode, RetrieveNode, GenerateNode


def create_rag_agent(
        summarize: SummarizeNode,
        retrieve: RetrieveNode,
        generate: GenerateNode,
        checkpoint_saver: BaseCheckpointSaver
) -> CompiledGraph:
    workflow = (
        StateGraph(RAGState)
        .add_node("summarize", summarize)
        .add_node("retrieve", retrieve)
        .add_node("generate", generate)
        .add_edge(START, "summarize")
        .add_edge("summarize", "retrieve")
        .add_edge("retrieve", "generate")
        .add_edge("generate", END)
    )
    return workflow.compile(checkpointer=checkpoint_saver)


class ChatAgent(AIAgent):
    def __init__(
            self,
            summarize: SummarizeNode,
            retrieve: RetrieveNode,
            generate: GenerateNode,
            checkpoint_saver: BaseCheckpointSaver
    ) -> None:
        self.rag_agent = create_rag_agent(
            summarize=summarize,
            retrieve=retrieve,
            generate=generate,
            checkpoint_saver=checkpoint_saver
        )

    async def generate(self, user_message: UserMessage) -> AssistantMessage:
        config = {"configurable": {"thread_id": user_message.chat_id}}
        inputs = {"messages": [{"role": "human", "content": user_message.text}]}
        outputs = await self.rag_agent.ainvoke(inputs, config=config)
        last_message = outputs["messages"][-1]
        return AssistantMessage(chat_id=user_message.chat_id, text=last_message.content)
