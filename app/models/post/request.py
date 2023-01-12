import re

from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class PostRequest(BaseModel):
    content: str

    @validator("content")
    def _content(cls, value):
        if re.compile(r"^([A-Za-z0-9]).{3,}$").match(value):
            return value
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid content")


class PostRequestPatch(PostRequest):
    ...
