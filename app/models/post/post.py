import re
from datetime import datetime

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
    date = ormar.Date(default=datetime.today().date())
    time = ormar.Time(default=datetime.today().time())
    content = ormar.Text(nullable=False)

    @validator("content")
    def _content(cls, value):

        if re.compile(r"^([A-Za-z0-9]).{3,}$").match(value):
            return value
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid content")
