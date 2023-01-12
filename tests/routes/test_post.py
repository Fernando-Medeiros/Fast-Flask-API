from typing import List

import pytest
from fastapi.testclient import TestClient

from ..utils.post import CaseCreate

case = CaseCreate()


# POST VALID (AUTH Required)
@pytest.mark.post
def test_post_valid(client_two_header_auth: TestClient):
    response = client_two_header_auth.post("/api/posts", json=case.valid_content)
    context = response.json()

    assert response.status_code == 201
    assert [context[attr] for attr in case.valid_content]


# POST INVALID (AUTH Required)
@pytest.mark.post
def test_post_invalid(client_two_header_auth: TestClient):
    response = client_two_header_auth.post("/api/posts", json=case.invalid_content)

    assert response.status_code == 400


# POST INVALID (WITHOUT AUTH)
@pytest.mark.post
def test_post_invalid_without_auth(client_one: TestClient):
    response = client_one.post("/api/posts", json=case.invalid_content)

    assert response.status_code == 401
    assert response.json()["detail"]


# GET ALL POSTS
@pytest.mark.post
def test_get_all_posts(client_three: TestClient):
    response = client_three.get("/api/posts")
    context = response.json()

    assert response.status_code == 200
    assert issubclass(type(context), List)
    assert len(context) > 0


# GET POST BY ID
@pytest.mark.post
def test_get_post_by_id(client_three: TestClient):
    response = client_three.get(f"/api/posts/{1}")

    assert response.status_code == 200
    assert response.json()["content"]


# GET POST BY ID WITHOUT POSTS IN DATABASE
@pytest.mark.post
def test_get_post_by_id_without_posts(client_one: TestClient):
    response = client_one.get(f"/api/posts/{1}")

    assert response.status_code == 404
    assert response.json()["detail"]


# GET POST BY USERNAME
@pytest.mark.post
def test_get_post_by_username(client_three: TestClient):
    response = client_three.get(f'/api/posts/user/{"marciaSouza"}')

    assert response.status_code == 200
    assert issubclass(type(response.json()), list)
    assert issubclass(type(response.json()[0]["id"]), int)


# GET POST BY USERNAME
@pytest.mark.post
def test_get_post_by_username_without_user(client: TestClient):
    response = client.get(f'/api/posts/user/{"marciaSouza"}')

    assert response.status_code == 404
    assert response.json()["detail"]


# UPDATE VALID CONTENT (AUTH Required)
@pytest.mark.post
def test_update_valid_post_content(client_three: TestClient):
    response = client_three.patch(f"/api/posts/{1}", json=case.update_valid_content)

    assert response.status_code == 200
    assert response.json()["content"] == case.update_valid_content["content"]


# UPDATE INVALID CONTENT (AUTH Required)
@pytest.mark.post
def test_update_invalid_post_content(client_three: TestClient):
    response = client_three.patch(f"/api/posts/{1}", json=case.update_invalid_content)

    assert response.status_code == 400


# DELETE (AUTH Required)
@pytest.mark.post
def test_delete_post(client_three: TestClient):
    response = client_three.delete(f"/api/posts/{1}")

    assert response.status_code == 200
