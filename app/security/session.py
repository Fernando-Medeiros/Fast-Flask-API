from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from werkzeug.security import check_password_hash
from app.helpers import Unauthorized
from app.models import ProfileModel, UserModel
from app.responses import TokenData

from ..repositories.backend import BackendDatabase
from .token import DecodeTokenJwt


class AuthBearer:
    url: str = "/api/v1/token"
    name: str = "JWT"
    auth_scheme = OAuth2PasswordBearer(tokenUrl=url, scheme_name=name)


def validate_credentials(token: str) -> TokenData:
    try:
        payload: dict = DecodeTokenJwt.decode(token)

        return TokenData(**payload)

    except JWTError:
        raise Unauthorized(
            "Could not validate credentials",
            {"WWW-Authenticate": "Bearer"},
        )


async def authenticate_user(email, password) -> UserModel:
    user = await BackendDatabase.get_or_none(UserModel, email=email)

    if user and check_password_hash(user.password, password):
        return user

    raise Unauthorized(
        "User not found or invalid password",
        {"WWW-Authenticate": "Bearer"},
    )


async def request_token(token: str = Depends(AuthBearer.auth_scheme)):
    payload = validate_credentials(token)

    return await BackendDatabase.get_or_404(ProfileModel, account=int(payload.sub))


async def session(current_user: ProfileModel = Depends(request_token)) -> ProfileModel:
    return current_user
