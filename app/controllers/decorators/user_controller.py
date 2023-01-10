from functools import wraps

import ormar
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel


def create_account(model: ormar.Model):
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
            entity = await model.objects.get_or_none(username=username)
            if entity:
                return entity
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Found'
            )

        return wrapper
    return inner


def get_account_data(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(current_user):
            return await model.objects.get(id=current_user.id)
                          
        return wrapper
    return inner


def update_user(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: BaseModel, current_user):
            
            entity = await model.objects.get(username=current_user.username)
            updates = request_model.dict(exclude_unset=True)
            return await entity.update(**updates)
        
        return wrapper
    return inner


def update_password(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: BaseModel, current_user):
            
            entity = await model.objects.get(username=current_user.username)
            updates = request_model.dict(exclude_unset=True)
            await entity.update(**updates)
            
            return {
                'status_code': status.HTTP_200_OK,
                'detail': 'Successfully updated password'
                }

        return wrapper
    return inner


def delete(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(current_user):
           
            if await model.objects.delete(username=current_user.username):
                return {
                    'status_code': status.HTTP_200_OK,
                    'detail': 'Account deleted'
                    }

        return wrapper
    return inner
