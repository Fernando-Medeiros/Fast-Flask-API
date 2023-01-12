from typing import List, Optional

import ormar
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserResponseAccountData(UserResponse):
    byear: Optional[str]
    bmonth: Optional[str]
    bday: Optional[str]
    created_at: ormar.DateTime
    access: List[str]
