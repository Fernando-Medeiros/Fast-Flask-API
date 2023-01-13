import datetime
from typing import List

from pydantic import BaseModel, validator


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserResponseAccountData(UserResponse):
    byear: str
    bmonth: str
    bday: str
    created_at: datetime.datetime
    access: List[str]

    @validator("created_at")
    def _create_at(cls, value):
        return value.strftime("%d/%m/%Y %H:%M:%S")
