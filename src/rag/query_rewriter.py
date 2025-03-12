from typing import TYPE_CHECKING, Union, Any, Optional

from langchain_core.runnables.utils import Input, Output

if TYPE_CHECKING:
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel, LLM
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import Runnable, RunnableConfig


class QueryRewriter(Runnable):
    def __init__(
            self,
            prompt: "BasePromptTemplate",
            model: Union["BaseChatModel", "LLM"],
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._chain = prompt | model | parser

    def invoke(self, query: str, **kwargs: Any) -> str:
        return self._chain.invoke({"query": query})

    async def ainvoke(
            self,
            input: Input,
            config: Optional[RunnableConfig] = None,
            **kwargs: Any
    ) -> Output:
        return await self._chain.ainvoke(input, config, **kwargs)
