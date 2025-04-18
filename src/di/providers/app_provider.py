from dishka import Provider, provide, Scope, from_context

from src.ai_agent import BaseAgent
from src.repository import MessageRepository
from src.core.use_cases import ChatAssistant, ChatHistoryManager

from src.settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)

    @provide(scope=Scope.APP)
    async def get_chat_history_manager(self, message_repository: MessageRepository) -> ChatHistoryManager:
        return ChatHistoryManager(message_repository)
