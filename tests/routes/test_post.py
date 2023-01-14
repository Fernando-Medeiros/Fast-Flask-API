from typing import List

import pytest
from fastapi.testclient import TestClient

from ..utils.post import CaseCreate

case = CaseCreate()


@pytest.mark.post
class TestPost:
    # (AUTH REQUIRED) - VALID
    def test_post_valid(self, client_two_auth: TestClient):
        response = client_two_auth.post("/api/posts", json=case.valid_content)

        assert response.status_code == 201
        assert response.json().get("content")

    # (AUTH REQUIRED) - INVALID
    def test_post_invalid(self, client_two_auth: TestClient):
        response = client_two_auth.post("/api/posts", json=case.invalid_content)

        assert response.status_code == 400

    # (WITHOUT AUTH) - INVALID
    def test_post_invalid_without_auth(self, client_one: TestClient):
        response = client_one.post("/api/posts", json=case.invalid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.post
class TestGet:
    def test_get_all_posts(self, client_three: TestClient):
        response = client_three.get("/api/posts")
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), List)
        assert len(context) > 0

    def test_get_post_by_id(self, client_three: TestClient):
        response = client_three.get(f"/api/posts/{1}")

        assert response.status_code == 200
        assert response.json().get("content")

    def test_get_posts_by_username(self, client_three: TestClient):
        response = client_three.get(f'/api/posts/user/{"marciaSouza"}')

        assert response.status_code == 200
        assert issubclass(type(response.json()), list)
        assert issubclass(type(response.json()[0]["id"]), int)

    # (WITHOUT POSTS or USERS)
    def test_get_post_by_id_without_posts(self, client_one: TestClient):
        response = client_one.get(f"/api/posts/{1}")

        assert response.status_code == 404
        assert response.json().get("detail")

    def test_get_post_by_username_without_user(self, client: TestClient):
        response = client.get(f'/api/posts/user/{"marciaSouza"}')

        assert response.status_code == 404
        assert response.json().get("detail")


@pytest.mark.post
class TestUpdate:
    # (AUTH REQUIRED) - VALID
    def test_update_valid_content(self, client_three: TestClient):
        response = client_three.patch(f"/api/posts/{1}", json=case.update_valid_content)

        assert response.status_code == 200
        assert response.json().get("content") == case.update_valid_content["content"]

    # (AUTH REQUIRED) - INVALID
    def test_update_invalid_content(self, client_three: TestClient):
        response = client_three.patch(
            f"/api/posts/{1}", json=case.update_invalid_content
        )

        assert response.status_code == 400


@pytest.mark.post
class TestDelete:
    # (AUTH REQUIRED)
    def test_delete_post(self, client_three: TestClient):
        response = client_three.delete(f"/api/posts/{1}")

        assert response.status_code == 200
