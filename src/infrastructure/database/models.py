from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import DateTime, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )


class MessageModel(BaseModel):
    __tablename__ = "messages"

    chat_id: Mapped[str]
    role: Mapped[str]
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="check_role_values"),
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"role={self.role}, "
            f"text={self.text}, "
            f"created_at={self.created_at})"
        )

    def __repr__(self) -> str:
        return str(self)
