from functools import wraps

import ormar
from app.utils.token_jwt import CreateTokenJwt
from werkzeug.security import check_password_hash

from fastapi import Form, HTTPException


def post(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(request_model: ormar.Model):
            attr = request_model.dict(exclude_unset=True)
            user = model(**attr)
            return await user.save()

        return wrapper
    return inner


def post_login(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(email: str = Form(...), password: str = Form(...)):
            
            user = await model.objects.get_or_none(email=email)
            
            if not user or not check_password_hash(user.password, password):
                raise HTTPException(
                    status_code=403,
                    detail='User not found'
                )
            return {
                'access_token': CreateTokenJwt().create_token(id=user.id),
                'token_type': 'bearer'
            }
           
        return wrapper
    return inner

