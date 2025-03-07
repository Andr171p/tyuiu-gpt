from fastapi.responses import JSONResponse
from pydantic import BaseModel


class BasePresenter(BaseModel):
    def present(self) -> JSONResponse:
        raise NotImplemented
