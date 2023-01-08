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
    first_name = ormar.String(max_length=15, null=False)
    last_name = ormar.String(max_length=15, null=False)
    username = ormar.String(max_length=30, unique=True, null=False)
    email = ormar.String(max_length=100, unique=True, null=False)
    password = ormar.String(max_length=255, null=False)
    access = ormar.JSON(default=['user'])


    @validator('email')
    def validate_email(cls, value):
        if not re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+').match(value):
            raise HTTPException(status_code=400, detail='The user email format is invalid!')
        return value


    @validator('first_name')
    def validate_first_name(cls, value):
        if not re.compile(
            r'^[A-Za-z]+[A-Za-z]$').match(value):
            raise HTTPException(status_code=400, detail='The first name format is invalid!')
        return value
    

    @validator('last_name')
    def validate_last_name(cls, value):
        if not re.compile(
            r'^[A-Za-z]+[A-Za-z]$').match(value):
            raise HTTPException(status_code=400, detail='The last name format is invalid!')
        return value

    @validator('username')
    def validate_username(cls, value):
        if not re.compile(
            r'^[A-Za-z]+[A-Za-z]$').match(value):
            raise HTTPException(status_code=400, detail='The username format is invalid!')
        return value