from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


class UserRequest(BaseModel):
    name: str
    email: str
    password: str

    @validator('password', pre=True)
    def hash(cls, value):
        return  generate_password_hash(value)