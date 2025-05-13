from typing import Literal

from pathlib import Path


# Base project directory:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"  # environment variables

# Pagination constants:
DEFAULT_PAGE = 1
MIN_PAGE = 1
DEFAULT_LIMIT = 10
MIN_LIMIT = 1

# Postgres drivers:
PG_DRIVER: Literal["asyncpg"] = "asyncpg"

# Ensemble retriever weights:
SIMILARITY_WEIGHT = 0.6
BM25_WEIGHT = 0.4

# Models:
YANDEX_GPT_PRO = "yandexgpt"
GIGACHAT_MAX = "GigaChat-Max"

# Elasticsearch indices:
VECTOR_STORE_INDEX = "tyuiu_index"
BM25_INDEX = "docs-tyuiu-index"
