from functools import wraps

import ormar


def post(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: ormar.Model):
            attr = request_model.dict(exclude_unset=True)
            user = model(**attr)
            return await user.save()

        return wrapper
    return inner


def get(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper():
            return 'Hello World'

        return wrapper
    return inner


def patch(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return 'Hello World'

        return wrapper
    return inner


def delete(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return 'Hello World'

        return wrapper
    return inner
