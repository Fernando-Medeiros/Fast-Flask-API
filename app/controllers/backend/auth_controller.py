import ormar
from fastapi import HTTPException, status

from app.models.token import Token, TokenData
from app.models.user import UserModel
from app.utils.login_required import (
    authenticate_user,
    validate_credentials,
    validate_user,
)
from app.utils.token_jwt import TokenJwt

model: ormar.Model = UserModel


async def token(form_data):
    user: UserModel = await authenticate_user(form_data)
    return Token(
        access_token=TokenJwt.create_access_token(
            id=user.id,
            username=user.username,
            fresh=True,
        ),
        refresh_token=TokenJwt.create_refresh_token(
            id=user.id,
            username=user.username,
        ),
        token_type="bearer",
    )


async def refresh_token(form_data):
    try:
        data: TokenData = validate_credentials(form_data.refresh_token)
        user: UserModel = await validate_user(data)
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="token cannot be validated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return Token(
            access_token=TokenJwt.create_access_token(
                id=user.id,
                username=user.username,
                fresh=False,
            ),
            refresh_token=TokenJwt.create_refresh_token(
                id=user.id,
                username=user.username,
            ),
            token_type="bearer",
        )
