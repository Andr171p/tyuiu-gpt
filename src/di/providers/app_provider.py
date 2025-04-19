from dishka import Provider, provide, Scope, from_context

from src.core.interfaces import BaseAIAgent
from src.core.use_cases import ChatAssistant

from src.settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAIAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)
