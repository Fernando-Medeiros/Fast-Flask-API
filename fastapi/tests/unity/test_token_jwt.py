from datetime import datetime

from app.utils.token_jwt import CreateTokenJwt, DecodeTokenJwt

from ..utils.token import TestToken

token = CreateTokenJwt()
utils = TestToken()


def test_token_expire() -> None:
    expire = token.expire()
    
    assert type(expire) == datetime
    assert expire.day == datetime.utcnow().day
    assert expire.hour != datetime.utcnow().hour


def test_token_body() -> None:
    context = utils.create_context()
    body = token.body(**context)

    assert [body[key] for key in context]


def test_token_create() -> None:
    context = utils.create_context()
    create_token = token.create_token(**context)

    assert type(create_token) == str
    assert len(create_token) > 200


def test_token_decode() -> None:
    context = utils.create_context()
    create_token = token.create_token(**context)
    t_decode = DecodeTokenJwt().decode(create_token)
    
    assert [t_decode[key] for key in context]