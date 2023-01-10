import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    @validator('password', pre=True)
    def validate_password(cls, value):
        
        def check_space() -> bool:
            return ' ' in [char for char in value if char == ' ']

        if not re.compile(r'^([A-Za-z0-9]).{7,}$').match(value) or check_space():
            raise HTTPException(status_code=400, detail='The password format is invalid!')
        
        return generate_password_hash(value)


class UserRequestPatch(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


class UserRequestUpdatePassword(BaseModel):
    password: Optional[str]

    @validator('password', pre=True)
    def validate_password(cls, value):
        
        def check_space() -> bool:
            return ' ' in [char for char in value if char == ' ']

        if not re.compile(r'^([A-Za-z0-9]).{7,}$').match(value) or check_space():
            raise HTTPException(status_code=400, detail='The password format is invalid!')
        
        return generate_password_hash(value)
