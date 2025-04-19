from datetime import datetime

from pydantic import BaseModel


class DateToCountDTO(BaseModel):
    date: datetime
    count: int
