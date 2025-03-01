import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")


class EmbeddingsSettings(BaseSettings):
    model_name: str = "ai-forever/sbert_large_nlu_ru"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {'normalize_embeddings': False}


class ElasticSettings(BaseSettings):
    host: str = os.getenv("ELASTIC_HOST")
    user: str = os.getenv("ELASTIC_USER")
    password: str = os.getenv("ELASTIC_PASSWORD")


class Neo4jSettings(BaseSettings):
    uri: str = os.getenv("NEO4J_URI")


class GigachatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")
    model_name: str = os.getenv("GIGACHAT_MODEL_NAME")
    prompt: str = os.path.join(BASE_DIR, "prompts", "Сотрудник_приёмной_комиссии.txt")


class YandexGPTSettings(BaseSettings):
    folder_id: str = os.getenv("YANDEX_FOLDER_ID")
    api_key: str = os.getenv("YANDEX_GPT_API_KEY")


class Settings(BaseSettings):
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elastic: ElasticSettings = ElasticSettings()
    neo4j: Neo4jSettings = Neo4jSettings()
    gigachat: GigachatSettings = GigachatSettings()
    yandexgpt: YandexGPTSettings = YandexGPTSettings()


settings = Settings()
