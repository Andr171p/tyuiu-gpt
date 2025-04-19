from dishka import make_async_container

from src.di.providers import (
    AppProvider,
    RabbitProvider,
    AIAgentProvider,
    DatabaseProvider,
    ConnectionsProvider
)
from src.settings import Settings


settings = Settings()

container = make_async_container(
    AppProvider(),
    RabbitProvider(),
    AIAgentProvider(),
    DatabaseProvider(),
    ConnectionsProvider(),
    context={Settings: settings}
)
