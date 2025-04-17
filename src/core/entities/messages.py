from enum import Enum

from pydantic import BaseModel


class Roles(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class UserMessage(BaseModel):
    role: str = Roles.USER
    chat_id: str
    text: str


class AssistantMessage(BaseModel):
    role: str = Roles.ASSISTANT
    text: str
