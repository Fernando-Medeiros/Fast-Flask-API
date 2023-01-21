import re

from fastapi import HTTPException
from pydantic import BaseModel, validator


class PostRequest(BaseModel):
    content: str

    @validator("content")
    def _content(cls, value):
        regex = r"^([A-Za-z0-9]).{3,1000}$"

        if re.compile(regex).match(value):
            return value

        raise HTTPException(400, "Invalid content")
