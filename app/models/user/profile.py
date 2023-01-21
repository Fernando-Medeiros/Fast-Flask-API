import re
from typing import Dict, Optional, Union

import ormar
from fastapi import HTTPException
from pydantic import validator

from setup import BaseMeta

from .user import UserModel

regex = {"username": r"^[A-Za-z]+[A-Za-z]$"}


class ProfileModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "profiles"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    account: Optional[Union[UserModel, Dict]] = ormar.ForeignKey(
        UserModel,
        related_name="profile",
        unique=True,
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    username = ormar.String(max_length=20, unique=True, nullable=False)
    avatar = ormar.String(max_length=255, nullable=False, default="default.png")
    bio = ormar.String(max_length=255, nullable=False, default="...")

    @validator("username")
    def _username(cls, value):
        if re.compile(regex["username"]).match(value):
            return value
        raise HTTPException(400, "Username format is invalid")
