from dishka import make_async_container

from src.di.providers import (
    AppProvider,
    AIAgentProvider,
    DatabaseProvider
)
from src.settings import Settings


settings = Settings()

container = make_async_container(
    AppProvider(),
    AIAgentProvider(),
    DatabaseProvider(),
    context={Settings: settings}
)
