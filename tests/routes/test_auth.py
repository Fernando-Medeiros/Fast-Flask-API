import pytest

from app.models.token import Token
from app.routes.security.token_jwt import DecodeTokenJwt
from tests.conftest import UrlToken
from tests.utils.user import CaseLogin


@pytest.mark.token
class TestToken:
    def test_auth_access_token(self, client_one):
        response = client_one.post(
            UrlToken.token, data=CaseLogin.login, headers=CaseLogin.content_type
        )
        tokens = Token(**response.json())

        assert response.status_code == 200
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type

    def test_auth_refresh_token(self, client_one):
        access_response = client_one.post(
            UrlToken.token, data=CaseLogin.login, headers=CaseLogin.content_type
        )
        refresh_response = client_one.post(
            UrlToken.refresh, json=access_response.json()
        )
        tokens = Token(**refresh_response.json())

        assert access_response.status_code == 200
        assert refresh_response.status_code == 200
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type


@pytest.mark.token
class TestHeaders:
    def test_header_authorization(self, client_two_auth):
        assert DecodeTokenJwt().decode(
            client_two_auth.headers.get("authorization").split(" ")[-1]
        )
