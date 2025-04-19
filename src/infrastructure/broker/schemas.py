from typing import List

from pydantic import BaseModel

from src.core.entities import BaseMessage


class MessagesToSaveSchema(BaseModel):
    messages: List[BaseMessage]
