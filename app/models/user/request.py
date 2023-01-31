import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


class Pwd(BaseModel):
    password: str

    @validator("password", pre=True)
    def _password(cls, value):
        regex = r"^([A-Za-z0-9]).{7,}$"

        if re.compile(regex).match(value) and " " not in value:
            return generate_password_hash(value)

        raise HTTPException(400, "Password format is invalid")


# CREATE
class RequestCreateAccount(Pwd):
    first_name: str
    last_name: str
    username: str
    email: str

    @validator("first_name", "last_name", pre=True)
    def _(cls, value: str):
        return value.casefold()


class RequestProfile(BaseModel):
    username: Optional[str]
    bio: str


class RequestBirthday(BaseModel):
    day: str
    month: str
    year: str

    @validator("day", "month", "year")
    def exclude_unset(cls, value):
        try:
            int(value)
        except:
            raise HTTPException(400, "Invalid data format")
        return value


class RequestAccess(BaseModel):
    access: str


# UPDATE
class UpdateAccount(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]

    @validator("first_name", "last_name", "email")
    def exclude_unset(cls, value):
        return None if value in ["string", " ", ""] else value


class UpdateProfile(BaseModel):
    username: Optional[str]
    bio: Optional[str]

    @validator("username", "bio")
    def exclude_unset(cls, value):
        return None if value == "string" else value


class UpdateAvatar(BaseModel):
    avatar: str

    @validator("avatar")
    def exclude_unset(cls, value):
        return None if value == "string" else value


class UpdateBackground(BaseModel):
    background: str

    @validator("background")
    def exclude_unset(cls, value):
        return None if value == "string" else value


class UpdateAccess(BaseModel):
    access: str


class UpdatePassword(Pwd):
    ...


class RecoverPassword(BaseModel):
    email: str
