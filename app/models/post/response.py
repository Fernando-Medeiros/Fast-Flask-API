import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, validator


class ResponseLike(BaseModel):
    user: Optional[Dict | List | str]

    @validator("user")
    def _author(cls, value):
        return {"username": value.get("username"), "avatar": value.get("avatar")}


class PostResponse(BaseModel):
    id: Optional[int]
    author: Optional[Dict | str]
    content: Optional[str]
    likes: Optional[List | int]
    replies: Optional[List | int]
    edit: Optional[bool]
    created_at: Optional[datetime.datetime | str]

    @validator("author")
    def _author(cls, value):
        return value.get("username")

    @validator("replies")
    def _replies(cls, value):
        return len(value)

    @validator("likes")
    def _likes(cls, value):
        return len(value)

    @validator("created_at")
    def _user(cls, value):
        return value.strftime("%d/%m/%Y %H:%M:%S")


class ResponseTimeline(PostResponse):
    @validator("replies")
    def _replies(cls, value):
        if not value:
            return len(value)
        return [PostResponse(**reply) for reply in value]

    @validator("likes")
    def _likes(cls, value):
        if not value:
            return len(value)
        return [ResponseLike(**likes) for likes in value]
