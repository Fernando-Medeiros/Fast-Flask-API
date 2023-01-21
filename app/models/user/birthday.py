from typing import Dict, Optional, Union

import ormar
from fastapi import HTTPException
from pydantic import validator

from setup import BaseMeta

from .profile import ProfileModel


class BirthdayModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "birthday"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="birthday",
        unique=True,
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    day = ormar.String(max_length=2, nullable=False)
    month = ormar.String(max_length=2, nullable=False)
    year = ormar.String(min_length=2, max_length=4, nullable=False)

    @validator("day", "month", "year")
    def _bday(cls, value):
        if str(value).isnumeric():
            return value
        raise HTTPException(400, "Date format is invalid, enter numbers only")
