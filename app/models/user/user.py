import re
from datetime import datetime

import ormar
from fastapi import HTTPException
from pydantic import validator

from setup import BaseMeta

regex = {
    "name": r"^[A-Za-z]+[A-Za-z]$",
    "email": r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+",
}


class UserModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    first_name = ormar.String(max_length=30, nullable=False)
    last_name = ormar.String(max_length=30, nullable=False)
    email = ormar.String(max_length=100, unique=True, nullable=False)
    password = ormar.String(max_length=255, nullable=False)
    created_at = ormar.DateTime(default=datetime.today, nullable=False)

    @validator("first_name", "last_name")
    def _first_name(cls, value):
        if re.compile(regex["name"]).match(value):
            return value
        raise HTTPException(400, "First or Last name format is invalid")

    @validator("email")
    def _email(cls, value):
        if re.compile(regex["email"]).match(value) and not " " in value:
            return value
        raise HTTPException(400, "Email format is invalid")
