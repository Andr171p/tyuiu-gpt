from src.core.entities import Chat
from src.infrastructure.database.models import ChatModel, MessageModel
from src.mappers.message_mapper import MessageMapper


class ChatMapper:
    @staticmethod
    def to_orm(chat: Chat) -> ChatModel:
        messages = [MessageModel(**message.model_dump()) for message in chat.messages]
        return ChatModel(chat_id=chat.chat_id, messages=messages)

    @staticmethod
    def from_orm(chat: ChatModel) -> Chat:
        messages = [MessageMapper.from_orm(message) for message in chat.messages]
        return Chat(chat_id=chat.chat_id, messages=messages)
