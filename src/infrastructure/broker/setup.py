from faststream.rabbit import RabbitBroker

from src.settings import RabbitSettings


def create_broker(rabbit_settings: RabbitSettings) -> RabbitBroker:
    return RabbitBroker(url=rabbit_settings.url)
