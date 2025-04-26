from typing import Literal

from pydantic import BaseModel


class BaseMessage(BaseModel):
    chat_id: str
    role: Literal["user", "assistant"]
    text: str

    class Config:
        from_attributes = True


class UserMessage(BaseMessage):
    role: str = "user"


class AssistantMessage(BaseMessage):
    role: str = "assistant"
