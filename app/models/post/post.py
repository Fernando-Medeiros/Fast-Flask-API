import re

import ormar
from fastapi import HTTPException, status
from pydantic import validator

from setup import database, metadata

from ..user import UserModel


class PostModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "posts"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    author = ormar.ForeignKey(
        UserModel,
        related_name="posts",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    like = ormar.Integer(default=0)
    date = ormar.Date(nullable=True)
    time = ormar.Time(nullable=True)
    response = ormar.Boolean(default=False)
    content = ormar.Text(nullable=False)

    @validator("content")
    def _content(cls, value):
        regex = r"^([A-Za-z0-9]).{3,}$"

        if re.compile(regex).match(value):
            return value

        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid content")
