from datetime import datetime, timedelta

import pytest
from jose.exceptions import ExpiredSignatureError

from app.utils.token_jwt import DecodeTokenJwt, TokenJwt

from ..utils.token import CaseToken


@pytest.mark.tokenJwt
class TestTokenJwt:
    context = CaseToken().create_context()

    def test_expire_minutes(self):
        expire = TokenJwt.expire(15)

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
        t_decode = DecodeTokenJwt.decode(token)

        assert [t_decode[key] for key in self.context]

    def test_expired(self):
        expire = datetime.utcnow() - timedelta(minutes=5)
        token = TokenJwt.create_access_token(exp=expire, **self.context)

        with pytest.raises(ExpiredSignatureError):
            DecodeTokenJwt.decode(token)
