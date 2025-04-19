from dishka import Provider, provide, Scope

from src.infrastructure.connection_managers import (
    BaseConnectionManager,
    InMemoryConnectionManager
)


class ConnectionsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> BaseConnectionManager:
        return InMemoryConnectionManager()
