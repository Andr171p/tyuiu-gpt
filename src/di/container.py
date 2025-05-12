from dishka import make_async_container

from src.di.providers import (
    AppProvider,
    DatabaseProvider,
    LangchainProvider,
    InfrastructureProvider
)
from src.tyuiu_gpt.settings import Settings


settings = Settings()

container = make_async_container(
    AppProvider(),
    AppProvider(),
    DatabaseProvider(),
    LangchainProvider(),
    InfrastructureProvider(),
    context={Settings: settings}
)
