from dishka import make_async_container

from src.di.providers import (
    AppProvider,
    AIAgentProvider,
    DatabaseProvider
)


container = make_async_container(
    AppProvider(),
    AIAgentProvider(),
    DatabaseProvider()
)
