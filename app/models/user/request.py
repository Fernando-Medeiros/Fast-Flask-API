import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


def validate_password(cls, value):
    regex = r"^([A-Za-z0-9]).{7,}$"
    if re.compile(regex).match(value) and " " not in value:
        return generate_password_hash(value)

    raise HTTPException(
        status.HTTP_400_BAD_REQUEST, detail="Password format is invalid"
    )


class RequestUpdatePassword(BaseModel):
    password: Optional[str] = None

    @validator("password", pre=True)
    def _password(cls, value):
        return validate_password(cls, value)


class UserRequest(RequestUpdatePassword):
    first_name: str
    last_name: str
    username: str
    email: str
    bday: str
    bmonth: str
    byear: str


class RequestUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    bday: Optional[str] = None
    bmonth: Optional[str] = None
    byear: Optional[str] = None


class RequestRecoverPassword(BaseModel):
    bday: str
    email: str
