from dishka import Provider, provide, Scope

from faststream.rabbit import RabbitBroker

from src.tyuiu_gpt.settings import Settings
from src.tyuiu_gpt.api.connection_managers import (
    BaseConnectionManager,
    InMemoryConnectionManager
)


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_rabbit_broker(self, settings: Settings) -> RabbitBroker:
        return RabbitBroker(url=settings.rabbit.url)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> BaseConnectionManager:
        return InMemoryConnectionManager()
