from src.rag import BaseRAG


class ChatBotService:
    def __init__(self, rag: BaseRAG) -> None:
        self._rag = rag

    async def answer(self, question: str) -> str:
        return await self._rag.generate(question)
