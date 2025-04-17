from datetime import datetime

from sqlalchemy import DateTime, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base_model import BaseModel
from src.infrastructure.database.models.chat_relation_mixin import ChatRelationMixin


class MessageModel(ChatRelationMixin, BaseModel):
    __tablename__ = "messages"

    _chat_back_populates = "messages"

    role: Mapped[str]
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="check_role_values"),
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, role={self.role}, text={self.text}, created_at={self.created_at})"

    def __repr__(self) -> str:
        return str(self)
