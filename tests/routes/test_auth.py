import pytest
from fastapi.testclient import TestClient

from app.models.token import Token
from app.routes.security.token_jwt import DecodeTokenJwt
from tests.utils.user import CaseLogin


@pytest.mark.token
class TestToken:
    def test_auth_access_token(self, client_one: TestClient):
        response = client_one.post(
            "/api/token", data=CaseLogin.login, headers=CaseLogin.content_type
        )
        tokens = Token(**response.json())

        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type
        assert response.status_code == 200

    def test_auth_refresh_token(self, client_one: TestClient):
        access_response = client_one.post(
            "/api/token", data=CaseLogin.login, headers=CaseLogin.content_type
        )
        refresh_response = client_one.post(
            "/api/refresh_token", json=access_response.json()
        )
        tokens = Token(**refresh_response.json())

        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type
        assert access_response.status_code == 200
        assert refresh_response.status_code == 200


@pytest.mark.token
class TestHeaders:
    def test_header_authorization(self, client_two_auth: TestClient):
        assert DecodeTokenJwt().decode(
            client_two_auth.headers.get("authorization").split(" ")[-1]
        )
