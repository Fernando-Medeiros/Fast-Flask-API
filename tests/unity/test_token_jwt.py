from datetime import datetime, timedelta

import pytest
from jose.exceptions import ExpiredSignatureError

from app.routes.security.token_jwt import DecodeTokenJwt, TokenJwt
from tests.utils.token import CaseToken


@pytest.mark.tokenJwt
class TestTokenJwt:
    context = CaseToken().create_context()

    def test_expire_minutes(self):
        expire = TokenJwt.expire(minutes=15)

        assert issubclass(type(expire), datetime)
        assert expire.minute != datetime.utcnow().minute

    def test_create_access_token(self):
        token = TokenJwt.create_access_token(**self.context)

        assert issubclass(type(token), str)
        assert len(token) > 150

    def test_create_refresh_token(self):
        token = TokenJwt.create_refresh_token()

        assert issubclass(type(token), str)
        assert len(token) > 150

    def test_decode(self):
        token = TokenJwt.create_access_token(**self.context)
        t_decode: dict = DecodeTokenJwt.decode(token)

        assert t_decode.get("sub")

    def test_expired(self):
        expire = datetime.utcnow() - timedelta(minutes=5)
        token = TokenJwt.create_access_token(exp=expire, **self.context)

        with pytest.raises(ExpiredSignatureError):
            DecodeTokenJwt.decode(token)
