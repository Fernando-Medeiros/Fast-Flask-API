import os
from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY: str = os.getenv("SECRET_KEY", "159753852456")
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS512")
ACCESS_MINUTES: float = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_MINUTES: float = float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "15"))
PWD_RECOVER_MINUTES: float = float(os.getenv("PWD_RECOVER_TOKEN_EXPIRE_MINUTES", "15"))


class TokenJwt:
    @staticmethod
    def expire(minutes: float):
        return datetime.utcnow() + timedelta(minutes=minutes)

    @classmethod
    def create_access_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(ACCESS_MINUTES), "scope": "access_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET_KEY, ALGORITHM)
        return token

    @classmethod
    def create_refresh_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(REFRESH_MINUTES), "scope": "refresh_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET_KEY, ALGORITHM)
        return token

    @classmethod
    def create_recover_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(PWD_RECOVER_MINUTES), "scope": "recover_pwd_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET_KEY, ALGORITHM)
        return token


class DecodeTokenJwt:
    @staticmethod
    def decode(token) -> dict:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
