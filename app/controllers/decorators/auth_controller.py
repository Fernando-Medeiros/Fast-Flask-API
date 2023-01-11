from functools import wraps

import ormar
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from werkzeug.security import check_password_hash

from app.utils.token_jwt import CreateTokenJwt


def post_token(model: ormar.Model):
    def inner(func):
        @wraps(func)
        async def wrapper(form_data: OAuth2PasswordRequestForm = Depends()):

            entity = await model.objects.get_or_none(email=form_data.username)

            if not entity or not check_password_hash(
                entity.password, form_data.password
            ):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    detail="User not found or invalid password",
                )
            return {
                "access_token": CreateTokenJwt().create_token(id=entity.id),
                "token_type": "bearer",
            }

        return wrapper

    return inner
