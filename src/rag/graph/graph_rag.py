from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.documents import Document
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG


class GraphRAG(BaseRAG):
    def __init__(
            self,
            nodes_retriever: "BaseRetriever",
            extract_page_content_func: Callable[[List["Document"]], List[str]],
            graph_retriever: "BaseRetriever",
            format_docs_func: Callable[[List["Document"]], str],
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._chain = (
            {
                "context": nodes_retriever |
                           extract_page_content_func |
                           graph_retriever |
                           format_docs_func,
                "query": RunnablePassthrough()
            } |
            prompt |
            model |
            parser
        )

    async def generate(self, query: str) -> str:
        result = await self._chain.ainvoke(query)
        return result
