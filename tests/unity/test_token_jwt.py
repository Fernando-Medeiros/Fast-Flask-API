from datetime import datetime

import pytest

from app.utils.token_jwt import CreateTokenJwt, DecodeTokenJwt

from ..utils.token import TestToken

token = CreateTokenJwt()
utils = TestToken()


@pytest.mark.tokenJwt
class TestTokenJwt:
    context = utils.create_context()

    def test_token_expire(self):
        expire = token.expire()

        assert type(expire) == datetime
        assert expire.hour != datetime.utcnow().hour

    def test_token_body(self):
        body = token.body(**self.context)

        assert [body[key] for key in self.context]

    def test_token_create(self):
        create_token = token.create_token(**self.context)

        assert type(create_token) == str
        assert len(create_token) > 200

    def test_token_decode(self):
        create_token = token.create_token(**self.context)
        t_decode = DecodeTokenJwt().decode(create_token)

        assert [t_decode[key] for key in self.context]
