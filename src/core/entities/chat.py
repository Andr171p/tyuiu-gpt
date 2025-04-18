from datetime import datetime

from typing import List

from pydantic import BaseModel

from src.core.entities.messages import BaseMessage


class Chat(BaseModel):
    chat_id: str
    messages: List[BaseMessage]


class ChatPage(BaseModel):
    total: int
    page: int
    limit: int
    chat_id: str
    messages: List[BaseMessage]


class DateToCount(BaseModel):
    date: datetime
    count: int


class MessagesDateToCount(BaseModel):
    distribution: List[DateToCount]


class ChatMessagesDateToCount(BaseModel):
    chat_id: str
    distribution: List[DateToCount]
