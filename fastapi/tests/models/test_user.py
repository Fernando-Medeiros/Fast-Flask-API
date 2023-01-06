import asyncio

import pytest
from app.models.user import UserModel, UserRequest, UserResponse
from tests.utils.user import CaseCreate
from werkzeug.security import check_password_hash

from fastapi import HTTPException

utils = CaseCreate()

# UserModel
@pytest.mark.userModel
def test_model_valid_user():
    attr: dict = utils.valid_user
    user = UserModel(**attr)


@pytest.mark.userModel
def test_model_invalid_user():
    with pytest.raises(HTTPException):
        attr: dict = utils.invalid_user()
        user = UserModel(**attr)


@pytest.mark.userModel
def test_model_save_user():
    attr: dict = utils.valid_user
    user = UserModel(**attr)
    event = asyncio.new_event_loop()
    
    assert event.run_until_complete(user.save()) == user


@pytest.mark.userModel
def test_model_delete_user():
    event = asyncio.new_event_loop()
    get_user = event.run_until_complete(UserModel.objects.get(id=2))
    
    assert get_user.id == 2
    event.run_until_complete(get_user.delete())

    with pytest.raises(Exception):
        event.run_until_complete(UserModel.objects.get(id=2))


# UserRequest 
@pytest.mark.userModel
@pytest.mark.userModelRequest
def test_model_user_request():
    attr: dict = utils.valid_user
    user = UserRequest(**attr)

    assert [user.dict()[key] == value for key, value in attr.items()]
    assert check_password_hash(user.password, attr['password'])


# UserResponse
@pytest.mark.userModel
@pytest.mark.userModelResponse
def test_model_user_response():
    attr: dict = utils.valid_user
    event = asyncio.new_event_loop()
    
    u_request = UserRequest(**attr)
    u_model = UserModel(**u_request.dict())
    new_user = event.run_until_complete(u_model.save())

    u_response = UserResponse(**new_user.dict())
    
    assert type(u_response.id) == int
    assert type(u_response.access) == list