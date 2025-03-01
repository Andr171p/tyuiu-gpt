from src.api_v1.container import Container
from src.chat_bot import ChatBot


container = Container()


def get_chat_bot() -> ChatBot:
    return container.chat_bot


print(get_chat_bot())