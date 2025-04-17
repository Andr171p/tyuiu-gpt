from typing import Literal


URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

ASYNC_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"

AVAILABLE_MODELS = Literal[
    "yandexgpt",
    "yandexgpt-lite"
]
