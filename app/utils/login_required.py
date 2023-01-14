import ormar
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from werkzeug.security import check_password_hash

from ..models.token import TokenData
from ..models.user import UserModel
from .token_jwt import DecodeTokenJwt

model: ormar.Model = UserModel


class AuthBearer:
    url: str = "/api/token"
    auth_scheme = OAuth2PasswordBearer(tokenUrl=url)


def validate_credentials(token: str) -> TokenData:
    try:

        payload: dict = DecodeTokenJwt.decode(token)
        return TokenData(**payload)

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def validate_user(payload: TokenData) -> UserModel:
    user = await model.objects.get_or_none(id=payload.id, username=payload.username)
    if user:
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")


async def authenticate_user(form_data) -> UserModel:
    try:
        user = await model.objects.get(email=form_data.username)
        if not check_password_hash(user.password, form_data.password):
            raise
        return user
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="user not found or invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def request_token(token: str = Depends(AuthBearer.auth_scheme)) -> UserModel:
    payload = validate_credentials(token)
    user = await validate_user(payload)
    return user


async def login_required(current_user: UserModel = Depends(request_token)):
    return current_user
