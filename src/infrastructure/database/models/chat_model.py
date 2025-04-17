from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.database.models.message_model import MessageModel

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base_model import BaseModel


class ChatModel(BaseModel):
    __tablename__ = "chats"

    chat_id: Mapped[str] = mapped_column(unique=True)
    messages: Mapped[list["MessageModel"]] = relationship(back_populates="chat")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
