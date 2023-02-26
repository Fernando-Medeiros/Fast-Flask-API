from typing import Dict, List, Optional

from pydantic import BaseModel, validator


class ProfileResponse(BaseModel):
    username: str
    avatar: str
    background: str
    bio: str


class AccountResponse(BaseModel):
    id: int
    username: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    bio: Optional[str]
    account: Optional[List | Dict]
    birthday: Optional[List | Dict]
    likes: Optional[List | Dict]
    posts: Optional[List | int]
    replies: Optional[List | int]
    access: Optional[List | str]

    @validator("account")
    def _user(cls, value):
        if value:
            exclude = ["password", "id"]
            [value.pop(item) for item in exclude]
            value["created_at"] = value.get("created_at").strftime("%d/%m/%Y %H:%M:%S")
        return value

    @validator("birthday")
    def _birthday(cls, value):
        if value:
            value[0].pop("id")
        return value

    @validator("posts", "likes", "replies")
    def _posts_replies_likes(cls, value):
        return len(value)

    @validator("access")
    def _access(cls, value):
        return value[0].get("access")
