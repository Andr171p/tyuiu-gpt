from dishka import Provider, provide, Scope

from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from langgraph.checkpoint.base import BaseCheckpointSaver

from src.ai_agent import BaseAgent, ReACTAgent
from src.ai_agent.tools import RetrievalTool

from src.core.use_cases import ChatAssistant

from src.misc.files import read_txt
from src.settings import settings


class ChatAssistantProvider(Provider):
    @provide(scope=Scope.APP)
    def get_retrieval_tool(self, retriever: BaseRetriever) -> RetrievalTool:
        return RetrievalTool(retriever)

    @provide(scope=Scope.APP)
    def get_react_agent(
            self,
            checkpoint_saver: BaseCheckpointSaver,
            retrieval_tool: RetrievalTool,
            model: BaseChatModel
    ) -> BaseAgent:
        return ReACTAgent(
            checkpoint_saver=checkpoint_saver,
            tools=[retrieval_tool],
            prompt_template=read_txt(r"C:\Users\andre\IdeaProjects\TyuiuAIChatBotAPI\prompts\ai_agent_prompt.txt"),
            model=model
        )

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)
