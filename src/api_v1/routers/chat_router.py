from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.services.chat_bot_service import ChatBotService
from src.api_v1.dependencies import get_chat_bot
from src.api_v1.schemas import GetAnswerOnQuestionSchema, AnswerResponse


chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["ChatBot"]
)


@chat_router.post(path="/", response_model=AnswerResponse)
async def get_answer_on_question(
        question: GetAnswerOnQuestionSchema,
        chat_bot: Annotated[ChatBotService, Depends(get_chat_bot)]
) -> JSONResponse:
    answer = await chat_bot.answer(question.question)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=AnswerResponse(answer=answer).model_dump()
    )
