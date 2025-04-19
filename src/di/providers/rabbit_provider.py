from dishka import Provider, provide, Scope

from faststream.rabbit import RabbitBroker

from src.settings import Settings


class RabbitProvider(Provider):
    @provide(scope=Scope.APP)
    def get_rabbit_broker(self, settings: Settings) -> RabbitBroker:
        return RabbitBroker(url=settings.rabbit.url)
