from datetime import datetime

from typing import List

from pydantic import BaseModel


class PerDayCount(BaseModel):
    count: int
    date: datetime


class CountToDateDistribution(BaseModel):
    distribution: List[PerDayCount]
