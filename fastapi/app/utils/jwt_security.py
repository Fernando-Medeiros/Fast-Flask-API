import os
from datetime import datetime, timedelta

from jose import jwt


class TokenJwt:
    SECRET_KEY: str = os.getenv('SECRET_KEY', '159753852456')
    ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS512')
    EXPIRE_HOURS: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_HOURS', '3'))

    def expire(self, hours: int = EXPIRE_HOURS) -> datetime:
        return datetime.utcnow() + timedelta(hours=hours)


    def body(self, **kwargs) -> dict:
        content = {'expire': str(self.expire())}   
        if kwargs:
            for key, value in kwargs.items():
                content[key] = value
        return content


    def create_token(self, **kwargs) -> str:
        to_encode: dict = self.body(**kwargs)
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encode_jwt