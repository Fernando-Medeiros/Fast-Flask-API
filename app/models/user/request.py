import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


def validate_password(cls, value):
    if re.compile(r"^([A-Za-z0-9]).{7,}$").match(value) and " " not in value:
        return generate_password_hash(value)

    raise HTTPException(
        status.HTTP_400_BAD_REQUEST, detail="Password format is invalid"
    )


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    byear: str
    bmonth: str
    bday: str
    password: str

    @validator("password", pre=True)
    def _password(cls, value):
        return validate_password(cls, value)


class UserRequestPatch(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


class UserRequestUpdatePassword(BaseModel):
    password: Optional[str]

    @validator("password", pre=True)
    def _password(cls, value):
        return validate_password(cls, value)
