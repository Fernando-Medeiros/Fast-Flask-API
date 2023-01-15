import pytest
from fastapi.testclient import TestClient

from tests.utils.user import CaseCreate, CaseLogin

case = CaseCreate()


@pytest.mark.user
class TestPost:
    invalid = {
        "first_name": case.invalid_user("first_name"),
        "last_name": case.invalid_user("last_name"),
        "email": case.invalid_user("email"),
        "username": case.invalid_user("username"),
        "password": case.invalid_user("password"),
    }

    def test_create_account(self, client: TestClient):
        data = case.valid_user
        response = client.post("/api/users", json=data)
        context = response.json()

        assert response.status_code == 201
        assert context.get("username") == data.get("username")

    # UNIQUE CONSTRAINTS
    def test_unique_username(self, client_one: TestClient):
        data = CaseLogin.valid_user
        response = client_one.post("/api/users", json=data)

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_unique_email(self, client_one: TestClient):
        data = CaseLogin.valid_user.copy()
        data.update(username="otherUsername")
        response = client_one.post("/api/users", json=data)

        assert response.status_code == 400
        assert response.json().get("detail")

    # INVALID DATA
    def test_post_invalid_first_name(self, client: TestClient):
        response = client.post("/api/users", json=self.invalid.get("first_name"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_post_invalid_last_name(self, client: TestClient):
        response = client.post("/api/users", json=self.invalid.get("last_name"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_post_invalid_email(self, client: TestClient):
        response = client.post("/api/users", json=self.invalid.get("email"))

        assert response.status_code == 400
        assert response.json().get("detail")

    def test_post_invalid_password(self, client: TestClient):
        response = client.post("/api/users", json=self.invalid.get("password"))

        assert response.status_code == 400
        assert response.json().get("detail")


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
        assert context.get("username") == "marciaSouza"

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
        assert response.json().get("detail")

    def test_get_account_data_without_auth(self, client_one: TestClient):
        response = client_one.get("/api/users/account_data/")

        assert response.status_code == 401
        assert response.json().get("detail")


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
        assert response.json().get("detail")

    def test_invalid_email(self, client_two_auth: TestClient):
        response = client_two_auth.patch("/api/users", json=self.i_data["email"])

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH)
    def test_password_without_auth(self, client_one: TestClient):
        response = client_one.patch(
            "/api/users/update_password", json=self.v_data["password"]
        )
        assert response.status_code == 401
        assert response.json().get("detail")

    def test_email_without_auth(self, client_one: TestClient):
        response = client_one.patch("/api/users", json=self.v_data["email"])

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.user
class TestDelete:

    # (AUTH REQUIRED)
    def test_delete_auth_user(self, client_two_auth: TestClient):
        f_response = client_two_auth.delete("/api/users")
        s_response = client_two_auth.delete("/api/users")

        assert f_response.status_code == 200
        assert s_response.status_code == 404
        assert f_response.json().get("detail")
        assert s_response.json().get("detail")

    # (WITHOUT AUTH)
    def test_delete_without_auth(self, client: TestClient):
        response = client.delete("/api/users")

        assert response.status_code == 401
        assert response.json().get("detail")
