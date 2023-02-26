import pytest

from app.responses import RefreshToken, Token, TokenData
from app.security.token import TokenJwt


@pytest.mark.tokenModel
class TestTokenModel:
    data = {
        "access_token": TokenJwt.create_access_token(),
        "refresh_token": TokenJwt.create_refresh_token(),
        "token_type": "bearer",
    }

    def test_token_model(self):
        token = Token(**self.data)

        assert token.access_token
        assert token.refresh_token
        assert token.token_type
        assert len(token.access_token) > 150

    def test_token_data_(self):
        token = TokenData(sub="1")

        assert token.sub

    def test_refresh_token(self):
        token = RefreshToken(**self.data)

        assert token.refresh_token
        assert len(token.refresh_token) > 150
