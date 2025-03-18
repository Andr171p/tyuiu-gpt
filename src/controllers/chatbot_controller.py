from src.core.use_cases import ChatBotUseCase
from src.schemas import QuestionPost, AnswerResponse


class ChatBotController:
    def __init__(self, chatbot_use_case: ChatBotUseCase) -> None:
        self._chatbot_use_case = chatbot_use_case

    async def get_answer_response(self, question_post: QuestionPost) -> AnswerResponse:
        answer = await self._chatbot_use_case.answer(question_post.question)
        return AnswerResponse.from_answer(answer)
