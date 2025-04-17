from dishka import make_async_container

from src.di.providers import LangchainProvider, ChatAssistantProvider


container = make_async_container(
    LangchainProvider(),
    ChatAssistantProvider()
)
