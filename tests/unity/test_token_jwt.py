from datetime import datetime, timedelta

import pytest
from jose.exceptions import ExpiredSignatureError

from app.routes.security.token_jwt import DecodeTokenJwt, TokenJwt


@pytest.mark.tokenJwt
class TestAccessToken:
    username = "Tester01"
    context = {"sub": username, "fresh": True}

    def test_expire_minutes(self):
        expire = TokenJwt.expire(minutes=15)

        assert issubclass(type(expire), datetime)
        assert expire.minute != datetime.utcnow().minute

    def test_create(self):
        token = TokenJwt.create_access_token(**self.context)

        assert issubclass(type(token), str)
        assert len(token) > 150

    def test_decode(self):
        token = TokenJwt.create_access_token(**self.context)
        payload: dict = DecodeTokenJwt.decode(token)

        assert issubclass(type(payload.get("exp")), int)
        assert issubclass(type(payload.get("fresh")), bool)
        assert issubclass(type(payload.get("scope")), str)
        assert payload.get("sub") == self.username

    def test_expired(self):
        expire = datetime.utcnow() - timedelta(minutes=5)
        token = TokenJwt.create_access_token(exp=expire, **self.context)

        with pytest.raises(ExpiredSignatureError):
            DecodeTokenJwt.decode(token)


@pytest.mark.tokenJwt
class TestRefreshToken:
    username = "Tester02"
    context = {"sub": username, "fresh": False}

    def test_create(self):
        token = TokenJwt.create_refresh_token()

        assert issubclass(type(token), str)
        assert len(token) > 150

    def test_decode(self):
        token = TokenJwt.create_refresh_token(**self.context)
        payload: dict = DecodeTokenJwt.decode(token)

        assert issubclass(type(payload.get("exp")), int)
        assert issubclass(type(payload.get("fresh")), bool)
        assert issubclass(type(payload.get("scope")), str)
        assert payload.get("sub") == self.username

    def test_expired(self):
        expire = datetime.utcnow() - timedelta(minutes=5)
        token = TokenJwt.create_refresh_token(exp=expire, **self.context)

        with pytest.raises(ExpiredSignatureError):
            DecodeTokenJwt.decode(token)


@pytest.mark.tokenJwt
class TestRecoverToken:
    username = "Tester03"
    context = {"sub": username}

    def test_create(self):
        token = TokenJwt.create_recover_token()

        assert issubclass(type(token), str)
        assert len(token) > 150

    def test_decode(self):
        token = TokenJwt.create_recover_token(**self.context)
        payload: dict = DecodeTokenJwt.decode(token)

        assert issubclass(type(payload.get("exp")), int)
        assert issubclass(type(payload.get("scope")), str)
        assert payload.get("sub") == self.username

    def test_expired(self):
        expire = datetime.utcnow() - timedelta(minutes=5)
        token = TokenJwt.create_recover_token(exp=expire, **self.context)

        with pytest.raises(ExpiredSignatureError):
            DecodeTokenJwt.decode(token)
