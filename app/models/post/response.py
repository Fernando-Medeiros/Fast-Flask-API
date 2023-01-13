import datetime
from typing import Optional

from pydantic import BaseModel, validator


class PostResponse(BaseModel):
    id: Optional[int]
    content: Optional[str]
    date: datetime.date
    time: datetime.time
    like: Optional[int]
    response: Optional[bool]

    @validator("date")
    def _date(cls, value):
        return value.strftime("%d/%m/%Y")

    @validator("time")
    def _time(cls, value):
        return value.strftime("%H:%M:%S")
