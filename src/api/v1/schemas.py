from typing import List

from pydantic import BaseModel

from src.dto import CreationDateCount
from src.core.entities import BaseMessage


class ChatResponse(BaseModel):
    chat_id: str
    messages: List[BaseMessage]


class ChatPageResponse(BaseModel):
    total: int
    page: int
    limit: int
    chat_id: str
    messages: List[BaseMessage]


class MessagesDateToCountSchema(BaseModel):
    distribution: List[CreationDateCount]
