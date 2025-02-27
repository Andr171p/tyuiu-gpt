import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")


class ElasticSettings(BaseSettings):
    host: str = os.getenv("ELASTIC_HOST")
    user: str = os.getenv("ELASTIC_USER")
    password: str = os.getenv("ELASTIC_PASSWORD")


class Neo4jSettings(BaseSettings):
    uri: str = os.getenv("NEO4J_URI")


class Settings(BaseSettings):
    elastic: ElasticSettings = ElasticSettings()
    neo4j: Neo4jSettings = Neo4jSettings()


settings = Settings()
