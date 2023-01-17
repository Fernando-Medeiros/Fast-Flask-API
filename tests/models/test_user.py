from datetime import datetime

import pytest
from fastapi import HTTPException
from werkzeug.security import check_password_hash

from app.models.user import (
    RequestUpdate,
    RequestUpdatePassword,
    UserModel,
    UserRequest,
    UserResponse,
    UserResponseAccountData,
)
from tests.utils.user import CaseCreate

case = CaseCreate()


@pytest.mark.userModel
class TestUserModel:
    def test_valid_usermodel(self):
        data: dict = case.valid_user
        user = UserModel(created_at=datetime.today(), **data)

        assert user.dict(include={*data.keys()})

    def test_invalid_usermodel(self):
        with pytest.raises(HTTPException):
            UserModel(**case.invalid_user())


@pytest.mark.userModelRequest
class TestUserRequest:
    def test_user_request(self):
        data: dict = case.valid_user
        request = UserRequest(**data)

        assert request.dict(include={*data.keys()})
        assert check_password_hash(str(request.password), data["password"])

    def test_user_request_patch(self):
        data: dict = case.valid_user
        request = RequestUpdate(**data)

        assert request.dict(include={*data.keys()})

    def test_user_request_password(self):
        data: dict = case.valid_user
        request = RequestUpdatePassword(**data)

        assert request.dict(include={*data.keys()})


@pytest.mark.userModelResponse
class TestUserResponse:
    def test_user_response(self):
        data: dict = case.valid_user
        response = UserResponse(**data)

        assert response.dict(include={*data.keys()})

    def test_user_response_account_data(self):
        data: dict = case.valid_user.copy()

        response = UserResponseAccountData(
            id=1, created_at=datetime.today(), access=["user"], **data
        )

        assert response.dict(include={*data.keys()})
