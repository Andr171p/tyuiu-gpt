from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.core.use_cases import ChatBotUseCase
from src.presentation.api.v1.schemas import UserMessageSchema
from src.presentation.api.v1.presenters import AnswerPresenter


chatbot_router = APIRouter(
    prefix="/api/v1/chatbot",
    tags=["ChatBot"],
    route_class=DishkaRoute
)


@chatbot_router.post(path="/", response_model=AnswerPresenter)
async def get_answer(
        user_message: UserMessageSchema,
        chatbot: FromDishka[ChatBotUseCase]
) -> JSONResponse:
    answer = await chatbot.answer(user_message.question)
    return AnswerPresenter(answer=answer).present()
