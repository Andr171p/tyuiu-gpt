from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.infrastructure.database.models.chat_model import ChatModel

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship


class ChatRelationMixin:
    _chat_id_nullable: bool = False
    _chat_id_unique: bool = False
    _chat_back_populates: Optional[str] = None

    @declared_attr
    def chat_id(cls) -> Mapped[str]:
        return mapped_column(
            ForeignKey("chats.chat_id"),
            unique=cls._chat_id_unique,
            nullable=cls._chat_id_nullable
        )
    @declared_attr
    def chat(cls) -> Mapped["ChatModel"]:
        return relationship(
            argument="ChatModel",
            back_populates=cls._chat_back_populates
        )
