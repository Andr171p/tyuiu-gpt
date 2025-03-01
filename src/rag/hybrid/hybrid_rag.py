from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.documents import Document
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG


class HybridRAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            format_docs_func: Callable[[List["Document"]], str],
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser"
    ) -> None:
        self._chain = (
            {
                "context": retriever | format_docs_func,
                "question": RunnablePassthrough()
            } |
            prompt |
            model |
            parser
        )

    async def generate(self, query: str) -> str:
        result = await self._chain.ainvoke(query)
        return result
