import re

import ormar
from fastapi import HTTPException, status
from pydantic import validator

from setup import database, metadata

l_access = ["admin", "user"]

regex = {
    "name": r"^[A-Za-z]+[A-Za-z]$",
    "username": r"^[A-Za-z]+[A-Za-z]$",
    "email": r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+",
}


class UserModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "users"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    first_name = ormar.String(max_length=30, nullable=False)
    last_name = ormar.String(max_length=30, nullable=False)
    username = ormar.String(max_length=20, unique=True, nullable=False)
    email = ormar.String(max_length=100, unique=True, nullable=False)
    bday = ormar.String(max_length=2, nullable=False)
    bmonth = ormar.String(max_length=2, nullable=False)
    byear = ormar.String(min_length=2, max_length=4, nullable=False)
    created_at = ormar.DateTime(nullable=False)
    password = ormar.String(max_length=255, nullable=False)

    access = ormar.JSON(default=["user"])

    @validator("first_name", "last_name")
    def _first_name(cls, value):
        if re.compile(regex["name"]).match(value):
            return value
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="First or Last name format is invalid"
        )

    @validator("username")
    def _username(cls, value):
        if re.compile(regex["username"]).match(value):
            return value
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Username format is invalid"
        )

    @validator("email")
    def _email(cls, value):
        if re.compile(regex["email"]).match(value):
            return value
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Email format is invalid"
        )

    @validator("bday", "bmonth", "byear")
    def _bday(cls, value):
        if str(value).isnumeric():
            return value
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Date format is invalid, enter numbers only",
        )
