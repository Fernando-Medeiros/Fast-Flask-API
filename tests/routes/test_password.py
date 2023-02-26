from datetime import datetime, timedelta

import pytest

from app.requests import RecoverPassword
from app.security.token import TokenJwt
from tests.conftest import UrlPassword
from tests.utils.client import CaseLogin


@pytest.mark.password
class TestRecover:
    v_data = RecoverPassword(**CaseLogin.data).dict()
    i_data = RecoverPassword(**CaseLogin.invalid_user()).dict()

    content_type = {"Content-Type": "application/x-www-form-urlencoded"}

    path = UrlPassword.recover

    # VALID
    def test_recover_send_email(self, client_one):
        response = client_one.post(
            self.path, data=self.v_data, headers=self.content_type
        )

        assert response.status_code == 200
        assert response.json().get("detail")

    # INVALID
    def test_recover_invalid_data(self, client_one):
        response = client_one.post(
            self.path, data=self.i_data, headers=self.content_type
        )

        assert response.status_code == 404
        assert response.json().get("detail")

    # WITHOUT USER
    def test_recover_without_user(self, client):
        response = client.post(self.path, data=self.v_data, headers=self.content_type)

        assert response.status_code == 404
        assert response.json().get("detail")


@pytest.mark.password
class TestUpdate:
    v_data: dict[str, str] = CaseLogin.get_one_valid_field("password")
    i_data: dict[str, str] = CaseLogin.get_one_invalid_field("password")

    content_type = {"Content-Type": "application/x-www-form-urlencoded"}

    path = UrlPassword.update

    # (AUTH REQUIRED) - VALID
    def test_update_password(self, client_two_auth):
        response = client_two_auth.patch(
            self.path, data=self.v_data, headers=self.content_type
        )

        assert response.status_code == 204

    # (AUTH REQUIRED) - INVALID
    def test_update_invalid_password(self, client_two_auth):
        response = client_two_auth.patch(
            self.path, data=self.i_data, headers=self.content_type
        )

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH)
    def test_update_without_auth(self, client_one):
        response = client_one.patch(
            self.path, data=self.v_data, headers=self.content_type
        )

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.password
class TestReset:
    expire = datetime.utcnow() - timedelta(minutes=5)

    v_token: str = TokenJwt.create_recover_token(sub="1")
    i_token: str = TokenJwt.create_recover_token(sub="1", exp=expire)

    v_data = {"password": "test123@@@@", "confirm": "test123@@@@"}
    i_data = {"password": " ", "confirm": " "}
    d_data = {"password": "Test@123", "confirm": "Test@123@@@"}

    content_type = {"Content-Type": "application/x-www-form-urlencoded"}

    path = UrlPassword.reset

    # VALID
    def test_reset_password(self, client_one):

        response = client_one.patch(
            self.path + self.v_token, data=self.v_data, headers=self.content_type
        )

        assert response.status_code == 204

    # INVALID PASSWORD
    def test_reset_invalid_password(self, client_one):

        response = client_one.patch(
            self.path + self.v_token, data=self.i_data, headers=self.content_type
        )

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_reset_different_password_and_confirmation(self, client_one):
        response = client_one.patch(
            self.path + self.v_token, data=self.d_data, headers=self.content_type
        )

        assert response.status_code == 400
        assert response.json().get("detail")

    # INVALID CREDENTIALS
    def test_reset_invalid_credentials(self, client_one):
        response = client_one.patch(
            self.path + self.i_token, data=self.v_data, headers=self.content_type
        )

        assert response.status_code == 401
        assert response.json().get("detail")
