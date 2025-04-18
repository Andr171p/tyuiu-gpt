from typing import Union

from langchain.prompts import ChatPromptTemplate

from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models.llms import LLM
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable


from src.ai_agent.base_agent import BaseAgent
from src.ai_agent.utils import format_documents


class RAGAgent(BaseAgent):
    def __init__(
            self,
            retriever: BaseRetriever,
            prompt_template: str,
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._retriever = retriever
        self._prompt_template = prompt_template
        self._model = model

    async def generate(self, thread_id: str, query: str) -> str:
        rag_chain = self._create_rag_chain()
        response = await rag_chain.ainvoke(query)
        return response

    def _create_rag_chain(self) -> Runnable:
        prompt = ChatPromptTemplate.from_template(self._prompt_template)
        rag_chain = (
                {
                    "context": self._retriever | format_documents,
                    "question": RunnablePassthrough()
                } |
                prompt |
                self._model |
                StrOutputParser()
        )
        return rag_chain
