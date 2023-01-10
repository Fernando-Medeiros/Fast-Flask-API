from functools import wraps

import ormar
from pydantic import BaseModel

from fastapi import status
from fastapi.exceptions import HTTPException


def post(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: ormar.Model):
            attr = request_model.dict(exclude_unset=True)
            entity = model(**attr)
            return await entity.save()

        return wrapper
    return inner


def get_all(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper():
            return await model.objects.all()

        return wrapper
    return inner


def get_by_username(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(username: str):
            return await model.objects.get(username=username)

        return wrapper
    return inner


def patch(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: BaseModel, current_user, **kwargs):
            if current_user.id:
                entity = await model.objects.get(username=current_user.username)
                updates = request_model.dict(exclude_unset=True)
                await entity.update(**updates)
                return status.HTTP_200_OK, 'Updated data'

            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
        
        return wrapper
    return inner


def delete(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(current_user, **kwargs):
           
            if await model.objects.delete(username=current_user.username):
                return status.HTTP_200_OK, 'Account deleted'

            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

        return wrapper
    return inner
