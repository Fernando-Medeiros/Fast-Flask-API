import re

from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash

from fastapi import HTTPException


class UserRequest(BaseModel):
    name: str
    email: str
    password: str

    @validator('password', pre=True)
    def validate_password(cls, value):
        
        if not re.compile(
            r'^[A-Z|a-z|0-9]').match(value):
            raise HTTPException(status_code=400, detail='The password format is invalid!' + value )
        
        return generate_password_hash(value)