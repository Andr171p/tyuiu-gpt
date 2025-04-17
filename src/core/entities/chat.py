from typing import List, Union

from pydantic import BaseModel

from src.core.entities.messages import UserMessage, AssistantMessage


class Chat(BaseModel):
    chat_id: str
    messages: List[Union[UserMessage, AssistantMessage]]


class ChatPage(BaseModel):
    total: int
    page: int
    limit: int
    chat_id: str
    messages: List[Union[UserMessage, AssistantMessage]]
