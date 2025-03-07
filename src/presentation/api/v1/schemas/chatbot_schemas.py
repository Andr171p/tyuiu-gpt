from pydantic import BaseModel


class UserMessageSchema(BaseModel):
    question: str
