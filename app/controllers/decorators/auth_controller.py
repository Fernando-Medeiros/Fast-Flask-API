from functools import wraps

import ormar
from app.utils.token_jwt import CreateTokenJwt
from werkzeug.security import check_password_hash

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


def post_token(model: ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrapper(form_data: OAuth2PasswordRequestForm = Depends()):
            
            user = await model.objects.get_or_none(email=form_data.username)
            
            if not user or not check_password_hash(user.password, form_data.password):
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