import asyncio

import pytest
from app.models.user import UserModel, UserRequest, UserResponse
from tests.utils.user import TestUser
from werkzeug.security import check_password_hash

from fastapi import HTTPException


# UserModel
def test_model_valid_user() -> None:
    attr: dict = TestUser().valid_user()
    user = UserModel(**attr)


def test_model_invalid_user() -> None:
    with pytest.raises(HTTPException):
        attr: dict = TestUser().invalid_user()
        user = UserModel(**attr)


def test_model_save_user() -> None:
    attr: dict = TestUser().valid_user()
    user = UserModel(**attr)
    event = asyncio.new_event_loop()
    event.run_until_complete(user.save())


def test_model_delete_user() -> None:
    event = asyncio.new_event_loop()
    get_user = event.run_until_complete(UserModel.objects.get(id=1))
    
    assert get_user.id == 1
    event.run_until_complete(get_user.delete())

    with pytest.raises(Exception):
        event.run_until_complete(UserModel.objects.get(id=1))


# UserRequest 
def test_model_user_request() -> None:
    attr: dict = TestUser().valid_user()
    user = UserRequest(**attr)

    assert user.email == attr['email']
    assert check_password_hash(user.password, attr['password'])


# UserResponse
def test_model_user_response() -> None:
    attr: dict = TestUser().valid_user()
    event = asyncio.new_event_loop()
    
    u_request = UserRequest(**attr)
    u_model = UserModel(**u_request.dict())
    new_user = event.run_until_complete(u_model.save())

    u_response = UserResponse(**new_user.dict())
    
    assert type(u_response.id) == int
    assert type(u_response.access) == list