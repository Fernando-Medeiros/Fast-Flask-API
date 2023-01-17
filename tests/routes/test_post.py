from typing import List

import pytest

from tests.conftest import UrlPosts
from tests.utils.post import CaseCreate
from tests.utils.user import CaseLogin

post = CaseCreate()


@pytest.mark.post
class TestPost:
    path = UrlPosts.create

    # (AUTH REQUIRED) - VALID
    def test_post_valid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.valid_content)

        assert response.status_code == 201
        assert response.json().get("content")

    # (AUTH REQUIRED) - INVALID
    def test_post_invalid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.invalid_content)

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH) - INVALID
    def test_post_invalid_without_auth(self, client_one):
        response = client_one.post(self.path, json=post.invalid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.post
class TestGet:
    username: str = CaseLogin.valid_user["username"]

    path_all = UrlPosts.get_all
    path_id = UrlPosts.get_post_id
    path_user = UrlPosts.get_posts_user

    def test_get_all_posts(self, client_three):
        response = client_three.get(self.path_all)
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), List)
        assert len(context) > 0

    def test_get_post_by_id(self, client_three):
        response = client_three.get(self.path_id + "1")

        assert response.status_code == 200
        assert response.json().get("content")

    def test_get_posts_by_username(self, client_three):
        response = client_three.get(self.path_user + self.username)

        assert response.status_code == 200
        assert issubclass(type(response.json()), list)
        assert issubclass(type(response.json()[0]["id"]), int)

    # (WITHOUT POSTS or USERS)
    def test_get_post_by_id_without_posts(self, client_one):
        response = client_one.get(self.path_id + "1")

        assert response.status_code == 404
        assert response.json().get("detail")

    def test_get_post_by_username_without_user(self, client):
        response = client.get(self.path_user + self.username)

        assert response.status_code == 404
        assert response.json().get("detail")


@pytest.mark.post
class TestUpdate:
    path = UrlPosts.update

    # (AUTH REQUIRED) - VALID
    def test_update_valid_content(self, client_three):
        response = client_three.patch(self.path + "1", json=post.update_valid_content)

        assert response.status_code == 200
        assert response.json().get("content") == post.update_valid_content["content"]

    # (AUTH REQUIRED) - INVALID
    def test_update_invalid_content(self, client_three):
        response = client_three.patch(self.path + "1", json=post.update_invalid_content)

        assert response.status_code == 400
        assert response.json().get("detail")


@pytest.mark.post
class TestDelete:
    path = UrlPosts.delete

    # (AUTH REQUIRED)
    def test_delete_post(self, client_three):
        response = client_three.delete(self.path + "1")

        assert response.status_code == 200
        assert response.json().get("detail")
