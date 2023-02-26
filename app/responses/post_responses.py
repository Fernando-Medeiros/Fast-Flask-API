import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, validator


class PostResponse(BaseModel):
    id: Optional[int]
    author: Optional[Dict]
    content: Optional[str]
    likes: Optional[List | int]
    replies: Optional[List | int]
    edit: Optional[bool]
    created_at: Optional[datetime.datetime | str]

    @validator("author")
    def _author(cls, value):
        return {
            "username": value.get("username"),
            "avatar": value.get("avatar"),
        }

    @validator("replies")
    def _replies(cls, value):
        return len(value)

    @validator("likes")
    def _likes(cls, value):
        return len(value)

    @validator("created_at")
    def _user(cls, value):
        return value.strftime("%d/%m/%Y %H:%M:%S")
