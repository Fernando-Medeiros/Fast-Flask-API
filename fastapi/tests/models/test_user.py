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
    
    assert [user.dict()[key] for key in attr]


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
    get_user = event.run_until_complete(UserModel.objects.all())
    id = event.run_until_complete(get_user[0].delete())
    
    with pytest.raises(Exception):
        event.run_until_complete(UserModel.objects.get(id=id))


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
    request = UserRequest(**attr)
    model = UserModel(**request.dict())
    model.id = 1
    response = UserResponse(**model.dict())
    
    assert [response.dict()[key] for key in model.dict() if key != 'password']
