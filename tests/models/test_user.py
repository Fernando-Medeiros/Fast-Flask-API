import pytest
from fastapi import HTTPException
from werkzeug.security import check_password_hash

from app.models.user import (
    AccountDataResponse,
    ProfileResponse,
    RequestCreateAccount,
    UpdateAccount,
    UpdatePassword,
    UserModel,
)
from tests.utils.client import CaseProfileModel, CaseUserModel


@pytest.mark.userModel
class TestUserModel:
    def test_valid_usermodel(self):
        data: dict = CaseUserModel.data
        user = UserModel(**data)

        assert user.dict(include={*data.keys()})

    def test_invalid_usermodel(self):
        with pytest.raises(HTTPException):
            UserModel(**CaseUserModel.invalid_user("first_name"))
            UserModel(**CaseUserModel.invalid_user("last_name"))
            UserModel(**CaseUserModel.invalid_user("email"))


@pytest.mark.userModelRequest
class TestUserRequest:
    def test_user_request(self):
        data: dict = CaseUserModel.data
        data.update(username="tester")
        request = RequestCreateAccount(**data)

        assert request.dict(include={*data.keys()})
        assert check_password_hash(str(request.password), data["password"])

    def test_user_request_patch(self):
        data: dict = CaseUserModel.data
        request = UpdateAccount(**data)

        assert request.dict(include={*data.keys()})

    def test_user_request_password(self):
        data: dict = CaseUserModel.data
        request = UpdatePassword(**data)

        assert request.dict(include={*data.keys()})


@pytest.mark.userModelResponse
class TestUserResponse:
    def test_user_response(self):
        data: dict = CaseProfileModel.data
        response = ProfileResponse(**data)

        assert response.dict(include={*data.keys()})

    def test_user_response_account_data(self):
        data: dict = CaseUserModel.data
        data.update(id=1)
        response = AccountDataResponse(**data)

        assert response.dict(include={*data.keys()})
