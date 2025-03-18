from pydantic import BaseModel


class QuestionPost(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str

    @classmethod
    def from_answer(cls, answer: str) -> "AnswerResponse":
        return cls(answer=answer)
