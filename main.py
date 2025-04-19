"""
from src.presentation.api.app import create_app


app = create_app()
"""

import asyncio

from src.di.container import container
from src.core.entities import UserMessage
from src.core.use_cases import ChatAssistant


async def main() -> None:
    chat_assistant = await container.get(ChatAssistant)
    user_message = UserMessage(chat_id="1", text="О чем мы говорили")
    message = await chat_assistant.answer(user_message)
    print(message)


if __name__ == "__main__":
    asyncio.run(main())
