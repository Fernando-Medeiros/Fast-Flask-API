import pytest

from tests.conftest import UrlUsers
from tests.utils.client import CaseCreate, CaseLogin


@pytest.mark.user
class TestPost:
    invalid = {
        "first_name": CaseCreate.invalid_user("first_name"),
        "last_name": CaseCreate.invalid_user("last_name"),
        "email": CaseCreate.invalid_user("email"),
        "username": CaseCreate.invalid_user("username"),
        "password": CaseCreate.invalid_user("password"),
    }

    path = UrlUsers.create

    def test_create_account(self, client):
        data = CaseCreate.data
        response = client.post(self.path, json=data)
        context = response.json()

        assert response.status_code == 201
        assert context.get("username") == data.get("username")

    # UNIQUE CONSTRAINTS
    def test_unique_username(self, client_one):
        data = CaseLogin.data
        response = client_one.post(self.path, json=data)

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_unique_email(self, client_one):
        data = CaseLogin.data.copy()
        data.update(username="otherUsername")

        response = client_one.post(self.path, json=data)

        assert response.status_code == 400
        assert response.json().get("detail")

    # INVALID DATA
    def test_invalid_first_name(self, client):
        response = client.post(self.path, json=self.invalid.get("first_name"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_invalid_last_name(self, client):
        response = client.post(self.path, json=self.invalid.get("last_name"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_invalid_email(self, client):
        response = client.post(self.path, json=self.invalid.get("email"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_invalid_password(self, client):
        response = client.post(self.path, json=self.invalid.get("password"))

        assert response.status_code == 400
        assert response.json().get("detail")


@pytest.mark.user
class TestGet:
    username: str = CaseLogin.data["username"]

    path_all = UrlUsers.get_profiles
    path_user = UrlUsers.get_profile
    path_data = UrlUsers.get_account

    def test_get_all_users(self, client_one):
        response = client_one.get(self.path_all)
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), list)
        assert context[0]

    def test_get_user_by_username(self, client_one):
        response = client_one.get(self.path_user + self.username)
        context = response.json()

        assert response.status_code == 200
        assert context.get("username") == self.username

    # (AUTH REQUIRED)
    def test_get_account_data(self, client_two_auth):
        response = client_two_auth.get(self.path_data)
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context["id"]), int)
        assert issubclass(type(context["username"]), str)

    # (WITHOUT AUTH or USERS)
    def test_get_by_username_without_users(self, client):
        response = client.get(self.path_user + self.username)

        assert response.status_code == 404
        assert response.json().get("detail")

    def test_get_account_data_without_auth(self, client_one):
        response = client_one.get(self.path_data)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.user
class TestUpdate:
    v_email: dict = CaseCreate.get_one_valid_field("email")
    i_email: dict = CaseCreate.get_one_invalid_field("email")

    path = UrlUsers.update_account

    # (AUTH REQUIRED) - VALID
    def test_valid_email(self, client_two_auth):
        response = client_two_auth.patch(self.path, json=self.v_email)

        assert response.status_code == 200
        assert response.json().get("detail")

    def test_invalid_email(self, client_two_auth):
        response = client_two_auth.patch(self.path, json=self.i_email)

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_email_without_auth(self, client_one):
        response = client_one.patch(self.path, json=self.v_email)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.user
class TestDelete:
    path = UrlUsers.delete

    # (AUTH REQUIRED)
    def test_delete_auth_user(self, client_two_auth):
        f_response = client_two_auth.delete(self.path)
        s_response = client_two_auth.delete(self.path)

        assert f_response.status_code == 200
        assert s_response.status_code == 404
        assert f_response.json().get("detail")
        assert s_response.json().get("detail")

    # (WITHOUT AUTH)
    def test_delete_without_auth(self, client):
        response = client.delete(self.path)

        assert response.status_code == 401
        assert response.json().get("detail")
