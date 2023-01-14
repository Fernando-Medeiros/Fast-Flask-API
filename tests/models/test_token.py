import pytest

from app.models.token import RefreshToken, Token, TokenData
from app.utils.token_jwt import TokenJwt

from ..utils.user import CaseLogin


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
        _data: dict = CaseLogin().valid_user
        _data.update(id=1)
        token = TokenData(**_data)

        assert token.id
        assert token.username

        with pytest.raises(Exception):
            [token.dict()[key] for key in _data]

    def test_refresh_token(self):
        token = RefreshToken(**self.data)

        assert token.refresh_token
        assert len(token.refresh_token) > 150
