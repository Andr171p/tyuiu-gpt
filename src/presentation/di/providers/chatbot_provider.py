from dishka import Provider, provide, Scope

from src.rag import BaseRAG
from src.core.use_cases import ChatBotUseCase
from src.controllers import ChatBotController


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_chatbot_use_case(self, rag: BaseRAG) -> ChatBotUseCase:
        return ChatBotUseCase(rag)

    @provide(scope=Scope.APP)
    def get_chatbot_controller(self, chatbot_use_case: ChatBotUseCase) -> ChatBotController:
        return ChatBotController(chatbot_use_case)
