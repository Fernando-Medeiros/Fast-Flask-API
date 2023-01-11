from functools import wraps

import ormar
from pydantic import BaseModel

from fastapi import HTTPException, status


def get_all(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper():
            return await model.objects.all()

        return wrapper
    return inner


def get_by_id(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(id: int):
            
            post = await model.objects.get_or_none(id=id)
            
            if post:
                return post

            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail='Id not found')

        return wrapper
    return inner


def get_by_username(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(username: str):
                
            entity = await model.objects.get_or_none(username=username)

            if entity:
                posts = await entity.posts.all()
                return posts
            
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail='Username not found')

        return wrapper
    return inner


def patch(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(id: int, request_model: BaseModel, current_user):
            if current_user.id:
                
                post = await current_user.posts.get_or_none(id=id)

                if post:
                    updates = request_model.dict(exclude_unset=True)
                    return await post.update(**updates)

            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
        
        return wrapper
    return inner


def post(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: BaseModel, current_user):
            if current_user.id:
                attr = request_model.dict(exclude_unset=True)
                post = model(author=current_user, **attr)
                return await post.save()

            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')

        return wrapper
    return inner


def delete(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(id: int, current_user):

            if await model.objects.delete(id=id, author=current_user.id):
                return status.HTTP_200_OK, 'Post deleted'

            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

        return wrapper
    return inner
