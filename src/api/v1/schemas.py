from typing import List

from pydantic import BaseModel

from src.dto import DateToCountDTO
from src.core.entities import BaseMessage


class ChatSchema(BaseModel):
    chat_id: str
    messages: List[BaseMessage]


class ChatPageSchema(BaseModel):
    total: int
    page: int
    limit: int
    chat_id: str
    messages: List[BaseMessage]


class MessagesDateToCountSchema(BaseModel):
    distribution: List[DateToCountDTO]
