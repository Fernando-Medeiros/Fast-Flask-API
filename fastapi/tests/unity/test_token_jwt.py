from datetime import datetime

from app.utils.jwt_security import TokenJwt
from jose import jwt

from ..utils.token import TestToken

token = TokenJwt()


def test_token_expire() -> None:
    expire = token.expire()
    
    assert type(expire) == datetime
    assert expire.day == datetime.utcnow().day
    assert expire.hour != datetime.utcnow().hour


def test_token_body() -> None:
    context = TestToken().create_context()
    body = token.body(**context)

    assert [body[key] for key in context]


def test_token_create() -> None:
    context = TestToken().create_context()
    create_token = token.create_token(**context)

    assert type(create_token) == str
    assert len(create_token) > 200


def test_token_decode() -> None:
    context = TestToken().create_context()
    create_token = token.create_token(**context)
    t_decode = jwt.decode(create_token, token.SECRET_KEY, token.ALGORITHM)
    
    assert t_decode['name'] == context['name']
    assert t_decode['id'] == context['id']