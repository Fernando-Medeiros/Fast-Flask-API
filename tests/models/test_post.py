from datetime import datetime

import pytest
from fastapi import HTTPException

from app.models.post import PostModel, PostRequest, PostResponse
from tests.utils.post import CaseCreate


@pytest.mark.postModel
class TestPostModel:
    v_data = CaseCreate.valid_content
    i_data = CaseCreate.invalid_content

    def test_valid_postmodel(self):
        post = PostModel(**self.v_data)

        assert post.dict(include={*self.v_data.keys()})

    def test_invalid_postmodel(self):
        with pytest.raises(HTTPException):
            PostModel(**self.i_data)


@pytest.mark.postModelRequest
class TestPostRequest:
    v_data = CaseCreate.valid_content

    def test_post_request(self):
        post = PostRequest(**self.v_data)

        assert post.content == self.v_data["content"]


@pytest.mark.postModelResponse
class TestPostResponse:
    v_data = CaseCreate.valid_content

    def test_post_response(self):
        request = PostRequest(**self.v_data)
        model = PostModel(
            id=1,
            date=datetime.today().date(),
            time=datetime.today().time(),
            **request.dict()
        )
        response = PostResponse(**model.dict())

        assert request.dict(include={*model.dict().keys()})
        assert model.dict(include={*response.dict().keys()})
