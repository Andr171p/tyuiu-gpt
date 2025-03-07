from fastapi import status
from fastapi.responses import JSONResponse

from src.presentation.api.v1.presenters.base_presenter import BasePresenter


class AnswerPresenter(BasePresenter):
    answer: str

    def present(self) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=self.model_dump(),
        )
