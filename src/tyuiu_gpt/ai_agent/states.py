from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # Сообщения пользователя
    question: str  # Вопрос пользователя с суммаризацией диалога
    documents: list[Document]  # Найденные документы из базы знаний
