from src.rag import BaseRAG


class ChatBot:
    def __init__(self, rag: BaseRAG) -> None:
        self._rag = rag

    async def answer(self, question: str) -> str:
        answer = await self._rag.generate(question)
        return answer
