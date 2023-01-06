from datetime import datetime

import pytest
from app.utils.token_jwt import CreateTokenJwt, DecodeTokenJwt

from ..utils.token import TestToken

token = CreateTokenJwt()
utils = TestToken()


@pytest.mark.tokenJwt
def test_token_expire():
    expire = token.expire()
    
    assert type(expire) == datetime
    assert expire.hour != datetime.utcnow().hour


@pytest.mark.tokenJwt
def test_token_body():
    context = utils.create_context()
    body = token.body(**context)

    assert [body[key] for key in context]


@pytest.mark.tokenJwt
def test_token_create():
    context = utils.create_context()
    create_token = token.create_token(**context)

    assert type(create_token) == str
    assert len(create_token) > 200


@pytest.mark.tokenJwt
def test_token_decode():
    context = utils.create_context()
    create_token = token.create_token(**context)
    t_decode = DecodeTokenJwt().decode(create_token)
    
    assert [t_decode[key] for key in context]