import ormar
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from werkzeug.security import check_password_hash

from app.models.token import TokenData
from app.models.user import UserModel

from .token_jwt import DecodeTokenJwt

model: ormar.Model = UserModel


class AuthBearer:
    url: str = "/token"
    name: str = "JWT"
    auth_scheme = OAuth2PasswordBearer(tokenUrl=url, scheme_name=name)


async def verify_unique_constraint(model, detail: str = "", **kwargs) -> None:
    if await model.objects.get_or_none(**kwargs):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


async def get_user_or_404(**kwargs) -> UserModel:
    user = await model.objects.get_or_none(**kwargs)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def validate_credentials(token: str) -> TokenData:
    try:
        payload: dict = DecodeTokenJwt.decode(token)
        return TokenData(username=payload.get("sub"))

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def authenticate_user(username, password) -> UserModel:
    try:
        user = await model.objects.get(email=username)
        if not check_password_hash(user.password, password):
            raise
        return user
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="User not found or invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def request_token(token: str = Depends(AuthBearer.auth_scheme)) -> UserModel:
    payload: TokenData = validate_credentials(token)
    user: UserModel = await get_user_or_404(username=payload.username)
    return user


async def login_required(current_user: UserModel = Depends(request_token)) -> UserModel:
    return current_user
