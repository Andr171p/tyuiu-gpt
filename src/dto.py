from datetime import datetime

from typing import Union

from pydantic import BaseModel

from src.core.entities import UserMessage, AssistantMessage
from src.infrastructure.database.models import MessageModel


class MessageMapper:
    @staticmethod
    def from_orm(message: MessageModel) -> Union[UserMessage, AssistantMessage]:
        if message.role == "user":
            return UserMessage.model_validate(message)
        else:
            return AssistantMessage.model_validate(message)


class CreationDateCount(BaseModel):
    date: datetime
    count: int
