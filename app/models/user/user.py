import re
from datetime import datetime

import ormar
from fastapi import HTTPException
from pydantic import validator

from setup import database, metadata

l_access = ['admin', 'user']

class UserModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = 'users'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    first_name = ormar.String(max_length=30, nullable=False)
    last_name = ormar.String(max_length=30, nullable=False)
    username = ormar.String(max_length=20, unique=True, nullable=False)
    email = ormar.String(max_length=100, unique=True, nullable=False)
    byear = ormar.String(max_length=4, nullable=True)
    bday = ormar.String(max_length=2 ,nullable=True)
    bmonth = ormar.String(max_length=2 ,nullable=True)
    created_at = ormar.DateTime(default=datetime.today())
    password = ormar.String(max_length=255, nullable=False)

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