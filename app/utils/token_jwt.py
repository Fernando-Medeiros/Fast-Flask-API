import os
from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY: str = os.getenv("SECRET_KEY", "159753852456")
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS512")
EXPIRE_HOURS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "1"))


class CreateTokenJwt:
    def expire(self, hours: int = EXPIRE_HOURS):
        return datetime.utcnow() + timedelta(hours=hours)

    def body(self, **kwargs) -> dict:
        content = {"exp": self.expire(), "scope": "access_token"}
        content.update(**kwargs)
        return content.copy()

    def create_token(self, **kwargs) -> str:
        to_encode: dict = self.body(**kwargs)
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encode_jwt


class DecodeTokenJwt:
    def decode(self, token) -> dict:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
