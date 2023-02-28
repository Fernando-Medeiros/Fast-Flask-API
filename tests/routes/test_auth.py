import pytest

from app.models.token import Token
from app.security.token import DecodeTokenJwt
from tests.conftest import UrlToken
from tests.utils.client import CaseLogin


@pytest.mark.token
class TestAccessToken:
    data, content = CaseLogin.login, CaseLogin.content_type

    path: str = UrlToken.token

    def test_auth_access_token(self, client_one):
        response = client_one.post(self.path, data=self.data, headers=self.content)
        tokens = Token(**response.json())

        assert response.status_code == 200
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type


@pytest.mark.token
class TestRefeshToken:
    data, content = CaseLogin.login, CaseLogin.content_type

    path_access: str = UrlToken.token
    path_refresh: str = UrlToken.refresh

    def test_auth_refresh_token(self, client_one):
        access_response = client_one.post(
            self.path_access, data=self.data, headers=self.content
        )
        refresh_response = client_one.post(
            self.path_refresh, data=access_response.json(), headers=self.content
        )
        assert refresh_response.status_code == 200
        tokens = Token(**refresh_response.json())

        assert access_response.status_code == 200
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type


@pytest.mark.token
class TestHeaders:
    def test_header_authorization(self, client_two_auth):
        token = client_two_auth.headers.get("authorization").split(" ")[-1]

        assert DecodeTokenJwt().decode(token)
