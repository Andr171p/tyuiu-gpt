from src.api_v1.container import Container
from src.services.chat_bot_service import ChatBotService


container = Container()


def get_chat_bot() -> ChatBotService:
    return container.chat_bot


print(get_chat_bot())