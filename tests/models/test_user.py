import asyncio
from datetime import datetime

import pytest
from fastapi import HTTPException
from werkzeug.security import check_password_hash

from app.models.user import (
    UserModel,
    UserRequest,
    UserRequestPatch,
    UserRequestUpdatePassword,
    UserResponse,
    UserResponseAccountData,
)
from tests.utils.user import CaseCreate

case = CaseCreate()
event = asyncio.new_event_loop()


@pytest.mark.userModel
class TestUserModel:
    def test_valid_usermodel(self):
        data: dict = case.valid_user
        user = UserModel(created_at=datetime.today(), **data)

        assert user.dict(include={*data.keys()})

    def test_invalid_usermodel(self):
        with pytest.raises(HTTPException):
            UserModel(**case.invalid_user())

    def test_create_user(self):
        data: dict = case.valid_user
        user = UserModel(created_at=datetime.today(), **data)

        assert event.run_until_complete(user.save()) == user

    def test_delete_user(self):
        user = event.run_until_complete(UserModel.objects.first())

        id: int = event.run_until_complete(user.delete())

        with pytest.raises(Exception):
            event.run_until_complete(UserModel.objects.get(id=id))


@pytest.mark.userModelRequest
class TestUserRequest:
    def test_user_request(self):
        data: dict = case.valid_user
        request = UserRequest(**data)

        assert request.dict(include={*data.keys()})
        assert check_password_hash(str(request.password), data["password"])

    def test_user_request_patch(self):
        data: dict = case.valid_user
        request = UserRequestPatch(**data)

        assert request.dict(include={*data.keys()})

    def test_user_request_password(self):
        data: dict = case.valid_user
        request = UserRequestUpdatePassword(**data)

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
