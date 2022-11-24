import re

import ormar
from pydantic import validator
from setup import database, metadata

from fastapi import HTTPException

l_access = ['admin', 'user']

class UserModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = 'users'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    name = ormar.String(max_length=50, null=False)
    email = ormar.String(max_length=100, unique=True, null=False)
    password = ormar.String(max_length=255, null=False)
    access = ormar.JSON(default=['user'])


    @validator('email')
    def validate_email(cls, value):
        if not re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+').match(value):
            raise HTTPException(status_code=400, detail='The user email format is invalid!')
        return value
