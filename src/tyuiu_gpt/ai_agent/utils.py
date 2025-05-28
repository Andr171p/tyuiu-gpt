from typing import Sequence

from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, HumanMessage


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def format_messages(messages: Sequence[BaseMessage]) -> str:
    return "\n\n".join(
        f"{'User' if isinstance(message, HumanMessage) else 'AI'}: {message.content}"
        for message in messages
    )


def create_llm_chain(template: str, model: BaseChatModel) -> Runnable:
    return (
        ChatPromptTemplate.from_template(template)
        | model
        | StrOutputParser()
    )
