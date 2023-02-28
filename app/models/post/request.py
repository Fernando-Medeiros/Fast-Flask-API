import re

from fastapi import HTTPException
from pydantic import BaseModel, validator


class PostRequest(BaseModel):
    content: str

    @validator("content")
    def _content(cls, value):
        if len(value) >= 3 and len(value) <= 1000:
            return value
        else:
            raise HTTPException(400, "Invalid content")
