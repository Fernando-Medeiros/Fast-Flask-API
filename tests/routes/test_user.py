import pytest
from fastapi.testclient import TestClient

from ..utils.user import CaseCreate

case = CaseCreate()


@pytest.mark.user
class TestPost:
    # POST CREATE ACCOUNT
    def test_post_valid_user(self, client: TestClient):
        body = case.valid_user
        response = client.post("/api/users", json=body)
        context = response.json()

        assert response.status_code == 201
        assert context["email"] == body["email"]

    # INVALID DATA
    def test_post_invalid_first_name(self, client: TestClient):
        body = case.invalid_user("first_name")
        response = client.post("/api/users", json=body)

        assert response.status_code == 400

    def test_post_invalid_email(self, client: TestClient):
        body = case.invalid_user("email")
        response = client.post("/api/users", json=body)

        assert response.status_code == 400

    def test_post_invalid_password(self, client: TestClient):
        body = case.invalid_user("password")
        response = client.post("/api/users", json=body)

        assert response.status_code == 400


@pytest.mark.user
class TestGet:
    def test_get_all_users(self, client_one: TestClient):
        response = client_one.get("/api/users")
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), list)
        assert context[0]

    def test_get_user_by_username(self, client_one: TestClient):
        response = client_one.get(f'/api/users/{"marciaSouza"}')
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context["id"]), int)

    # (AUTH REQUIRED)
    def test_get_account_data(self, client_two_auth: TestClient):
        response = client_two_auth.get("/api/users/account_data/")
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context["id"]), int)
        assert issubclass(type(context["created_at"]), str)

    # (WITHOUT AUTH or USERS)
    def test_get_by_username_without_users(self, client: TestClient):
        response = client.get(f'/api/users/{"marciaSouza"}')

        assert response.status_code == 404
        assert response.json()["detail"]

    def test_get_account_data_without_auth(self, client_one: TestClient):
        response = client_one.get("/api/users/account_data/")

        assert response.status_code == 401


@pytest.mark.user
class TestUpdate:
    v_data = {
        "email": case.get_one_valid_field("email"),
        "password": case.get_one_valid_field("password"),
    }
    i_data = {
        "email": case.get_one_invalid_field("email"),
        "password": case.get_one_invalid_field("password"),
    }

    # (AUTH REQUIRED) - VALID
    def test_valid_email(self, client_two_auth: TestClient):
        response = client_two_auth.patch("/api/users", json=self.v_data["email"])

        assert response.status_code == 200

    def test_valid_password(self, client_two_auth: TestClient):
        response = client_two_auth.patch(
            "/api/users/update_password", json=self.v_data["password"]
        )
        assert response.status_code == 200

    # (AUTH REQUIRED) - INVALID
    def test_invalid_password(self, client_two_auth: TestClient):
        response = client_two_auth.patch(
            "/api/users/update_password", json=self.i_data["password"]
        )
        assert response.status_code == 400

    def test_invalid_email(self, client_two_auth: TestClient):
        response = client_two_auth.patch("/api/users", json=self.i_data["email"])

        assert response.status_code == 400

    # (WITHOUT AUTH)
    def test_password_without_auth(self, client_one: TestClient):
        response = client_one.patch(
            "/api/users/update_password", json=self.v_data["password"]
        )
        assert response.status_code == 401

    def test_email_without_auth(self, client_one: TestClient):
        response = client_one.patch("/api/users", json=self.v_data["email"])

        assert response.status_code == 401


@pytest.mark.user
class TestDelete:

    # (AUTH REQUIRED)
    def test_delete_auth_user(self, client_two_auth: TestClient):
        response = client_two_auth.delete("/api/users")

        assert response.status_code == 200

    # (WITHOUT AUTH)
    def test_delete_without_auth(self, client: TestClient):
        response = client.delete("/api/users")

        assert response.status_code == 401
