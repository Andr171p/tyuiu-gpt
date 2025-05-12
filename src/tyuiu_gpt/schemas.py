from typing import Literal

from pydantic import BaseModel, ConfigDict


class BaseMessage(BaseModel):
    role: Literal["user", "assistant"]
    chat_id: str
    text: str

    model_config = ConfigDict(from_attributes=True)


class UserMessage(BaseMessage):
    role: str = "user"


class AssistantMessage(BaseMessage):
    role: str = "assistant"


class ChatPage(BaseModel):
    total: int
    page: int
    limit: int
    chat_id: str
    messages: list[BaseMessage]
