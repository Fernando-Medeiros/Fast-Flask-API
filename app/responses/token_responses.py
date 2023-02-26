from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = "bearer"


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    sub: str
