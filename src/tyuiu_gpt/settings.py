import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH, PG_DRIVER


load_dotenv(ENV_PATH)


class EmbeddingsSettings(BaseSettings):
    MODEL_NAME: str = "intfloat/multilingual-e5-large"
    MODEL_KWARGS: dict = {"device": "cpu"}
    ENCODE_KWARGS: dict = {'normalize_embeddings': False}


class ElasticsearchSettings(BaseSettings):
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST")
    ELASTIC_PORT: int = os.getenv("ELASTIC_PORT")
    ELASTIC_USER: str = os.getenv("ELASTIC_USER")
    ELASTIC_PASSWORD: str = os.getenv("ELASTIC_PASSWORD")

    @property
    def elasticsearch_url(self) -> str:
        return f"http://{self.ELASTIC_HOST}:{self.ELASTIC_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_USER: str = os.getenv("REDIS_USER")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"


class PostgresSettings(BaseSettings):
    PG_HOST: str = os.getenv("POSTGRES_HOST")
    PG_PORT: int = os.getenv("POSTGRES_PORT")
    PG_USER: str = os.getenv("POSTGRES_USER")
    PG_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    PG_DB: str = os.getenv("POSTGRES_DB")

    DRIVER: str = "asyncpg"

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+{PG_DRIVER}://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


class RabbitSettings(BaseSettings):
    RABBIT_HOST: str = os.getenv("RABBIT_HOST")
    RABBIT_PORT: int = os.getenv("RABBIT_PORT")
    RABBIT_USER: str = os.getenv("RABBIT_USER")
    RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD")

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}:{self.RABBIT_PORT}"


class GigaChatSettings(BaseSettings):
    API_KEY: str = os.getenv("GIGACHAT_API_KEY")
    SCOPE: str = os.getenv("GIGACHAT_SCOPE")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")



class Settings(BaseSettings):
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    rabbit: RabbitSettings = RabbitSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
