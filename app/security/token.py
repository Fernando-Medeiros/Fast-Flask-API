import os
from datetime import datetime, timedelta

from jose import jwt

SECRET: str = os.getenv("SECRET_KEY", "159753852456")
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS512")

EXPACCESS: float = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
EXPREFRESH: float = float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "15"))
EXPRECOVER: float = float(os.getenv("PWD_RECOVER_TOKEN_EXPIRE_MINUTES", "15"))


class TokenJwt:
    @staticmethod
    def expire(minutes: float):
        return datetime.utcnow() + timedelta(minutes=minutes)

    @classmethod
    def create_access_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(EXPACCESS), "scope": "access_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET, ALGORITHM)
        return token

    @classmethod
    def create_refresh_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(EXPREFRESH), "scope": "refresh_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET, ALGORITHM)
        return token

    @classmethod
    def create_recover_token(cls, **kwargs) -> str:
        data = {"exp": cls.expire(EXPRECOVER), "scope": "recover_pwd_token"}
        data.update(**kwargs)
        token = jwt.encode(data, SECRET, ALGORITHM)
        return token


class DecodeTokenJwt:
    @staticmethod
    def decode(token) -> dict:
        return jwt.decode(token, SECRET, ALGORITHM)
