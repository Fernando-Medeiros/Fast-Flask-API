from typing import List

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    access: List[str]