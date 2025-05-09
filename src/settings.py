import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class EmbeddingsSettings(BaseSettings):
    # model_name: str = "ai-forever/sbert_large_nlu_ru"
    model_name: str = "intfloat/multilingual-e5-large"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {'normalize_embeddings': False}


class ElasticsearchSettings(BaseSettings):
    host: str = os.getenv("ELASTIC_HOST")
    user: str = os.getenv("ELASTIC_USER")
    password: str = os.getenv("ELASTIC_PASSWORD")


class RedisSettings(BaseSettings):
    host: str = os.getenv("REDIS_HOST")
    port: int = os.getenv("REDIS_PORT")
    user: str = os.getenv("REDIS_USER")
    password: str = os.getenv("REDIS_PASSWORD")

    url: str = f"redis://{user}:{password}@{host}:{port}"


class PostgresSettings(BaseSettings):
    host: str = os.getenv("PG_HOST")
    port: int = os.getenv("PG_PORT")
    user: str = os.getenv("PG_USER")
    password: str = os.getenv("PG_PASSWORD")
    db: str = os.getenv("PG_DB")
    driver: str = "asyncpg"

    url: str = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{db}"


class RabbitSettings(BaseSettings):
    host: str = os.getenv("RABBIT_HOST")
    port: int = os.getenv("RABBIT_PORT")
    user: str = os.getenv("RABBIT_USER")
    password: str = os.getenv("RABBIT_PASSWORD")

    url: str = f"amqp://{user}:{password}@{host}:{port}"


class Neo4jSettings(BaseSettings):
    uri: str = os.getenv("NEO4J_URI")


class GigaChatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")
    model_name: str = os.getenv("GIGACHAT_MODEL_NAME")


class YandexGPTSettings(BaseSettings):
    folder_id: str = os.getenv("YANDEX_FOLDER_ID")
    api_key: str = os.getenv("YANDEX_GPT_API_KEY")


class PromptsSettings(BaseSettings):
    agent_prompt: Path = BASE_DIR / "prompts" / "ai_agent_prompt.txt"
    rag_prompt: str = os.path.join(BASE_DIR, "prompts", "Сотрудник_приёмной_комиссии.txt")
    query_rewriter_prompt: str = os.path.join(BASE_DIR, "prompts", "Перефразирование_запроса.txt")


class Settings(BaseSettings):
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    rabbit: RabbitSettings = RabbitSettings()
    neo4j: Neo4jSettings = Neo4jSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    prompts: PromptsSettings = PromptsSettings()
