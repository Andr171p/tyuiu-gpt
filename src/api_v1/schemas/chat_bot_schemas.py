from pydantic import BaseModel


class GetAnswerOnQuestionSchema(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
