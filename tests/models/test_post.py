import pytest

from app.models import PostModel
from app.requests import PostRequest
from app.responses import PostResponse
from tests.utils.post import CasePostCreate


@pytest.mark.postModel
class TestPostModel:
    v_data = CasePostCreate.valid_content
    i_data = CasePostCreate.invalid_content

    def test_valid_postmodel(self):
        post = PostModel(id=1, author=1, **self.v_data)

        assert post.dict(include={*self.v_data.keys()})


@pytest.mark.postModelRequest
class TestPostRequest:
    v_data = CasePostCreate.valid_content

    def test_post_request(self):
        post = PostRequest(**self.v_data)

        assert post.content == self.v_data["content"]


@pytest.mark.postModelResponse
class TestPostResponse:
    v_data = CasePostCreate.valid_content

    def test_post_response(self):
        request = PostRequest(**self.v_data)
        model = PostModel(id=1, author=1, **request.dict())
        response = PostResponse(**model.dict())

        assert request.dict(include={*model.dict().keys()})
        assert model.dict(include={*response.dict().keys()})
