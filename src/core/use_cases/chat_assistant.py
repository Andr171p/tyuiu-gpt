from src.ai_agent import BaseAgent
from src.core.entities import UserMessage, AssistantMessage


class ChatAssistant:
    def __init__(self, ai_agent: BaseAgent) -> None:
        self._ai_agent = ai_agent

    async def answer(self, user_message: UserMessage) -> AssistantMessage:
        generated = await self._ai_agent.generate(user_message.chat_id, user_message.text)
        return AssistantMessage(chat_id=user_message.chat_id, text=generated)
