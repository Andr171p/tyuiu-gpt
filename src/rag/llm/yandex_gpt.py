from typing import Optional, Any, List, Dict

from yandex_cloud_ml_sdk import YCloudML

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import ChatMessage


class YandexGPT(BaseChatModel):
    def __init__(
            self,
            api_key: str,
            folder_id: str,
            temperature: float = 0.7,
            model_name: str = "yandexgpt",
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._yandex_cloud_ml = YCloudML(
            folder_id=folder_id,
            auth=api_key,
        )
        self._yandex_cloud_ml = (
            self._yandex_cloud_ml
            .models
            .completions(model_name)
            .configure(temperature=temperature)
        )

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any
    ) -> ChatResult:
        messages: List[Dict[str, str]] = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                raise ValueError(f"Unsupported message type: {message}")
            messages.append({"role": role, "content": message.content})
        response = self._yandex_cloud_ml.run(messages)
        if not response or not response.get("result"):
            raise ValueError("No response from YandexGPT")
        result = response["result"]
        generations = [
            ChatGeneration(message=ChatMessage(
                role="assistant",
                content=result["alternatives"][0]["message"]["text"]
            ))
        ]
        return ChatResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "yandex-gpt"
