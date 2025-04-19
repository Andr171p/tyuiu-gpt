from typing import List

from pydantic import BaseModel

from src.core.entities import BaseMessage


class SaveMessagesSchema(BaseModel):
    messages: List[BaseMessage]
