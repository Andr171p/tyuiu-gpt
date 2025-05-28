from typing import Literal

from pathlib import Path


# Директория проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"  # Переменные окружения

# Пагинация:
DEFAULT_PAGE = 1
MIN_PAGE = 1
DEFAULT_LIMIT = 10
MIN_LIMIT = 1

# Драйверы для Postgres:
PG_DRIVER: Literal["asyncpg"] = "asyncpg"

# Веса для извлечения документов из разных индексов:
SIMILARITY_WEIGHT = 0.6
BM25_WEIGHT = 0.4

# Доступные LLM модели:
YANDEX_GPT_MODELS: Literal["yandexgpt"] = "yandexgpt"
GIGACHAT_MODELS: Literal["GigaChat-Max"] = "GigaChat-Max"

# Названия индексов:
VECTOR_STORE_INDEX = "tyuiu_index"
BM25_INDEX = "docs-tyuiu-index"
