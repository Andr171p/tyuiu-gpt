from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.controllers import ChatBotController
from src.schemas import QuestionPost, AnswerResponse


chatbot_router = APIRouter(
    prefix="/api/v1/chatbot",
    tags=["ChatBot"],
    route_class=DishkaRoute
)


@chatbot_router.post(
    path="/",
    response_model=AnswerResponse,
    status_code=status.HTTP_200_OK
)
async def answer(
        question_post: QuestionPost,
        chatbot_controller: FromDishka[ChatBotController]
) -> AnswerResponse:
    answer_response = await chatbot_controller.get_answer_response(question_post)
    return answer_response
