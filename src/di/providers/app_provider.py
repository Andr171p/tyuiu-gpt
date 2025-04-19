from dishka import Provider, provide, Scope, from_context

from src.core.interfaces import BaseAIAgent
from src.core.use_cases import ChatAssistant
from src.infrastructure.connection_managers import BaseConnectionManager, InMemoryConnectionManager

from src.settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAIAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> BaseConnectionManager:
        return InMemoryConnectionManager()
