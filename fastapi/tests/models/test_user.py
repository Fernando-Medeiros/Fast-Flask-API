import asyncio

import pytest
from app.models.user import UserModel, UserRequest, UserResponse
from tests.utils.user import CaseCreate
from werkzeug.security import check_password_hash

from fastapi import HTTPException

case = CaseCreate()


# UserModel - Valid
@pytest.mark.userModel
def test_model_valid_usermodel():
    attr: dict = case.valid_user
    user = UserModel(**attr)
    
    assert [user.dict()[key] for key in attr]


# UserModel - Invalid
@pytest.mark.userModel
def test_model_invalid_user():
    with pytest.raises(HTTPException):
        attr: dict = case.invalid_user()
        user = UserModel(**attr)


# Save Account
@pytest.mark.userModel
def test_model_save_user():
    attr: dict = case.valid_user
    user = UserModel(**attr)
    event = asyncio.new_event_loop()
    
    assert event.run_until_complete(user.save()) == user


# Delete Account
@pytest.mark.userModel
def test_model_delete_user():
    event = asyncio.new_event_loop()
    user = event.run_until_complete(UserModel.objects.first())
    
    id: int = event.run_until_complete(user.delete())
    
    with pytest.raises(Exception):
        event.run_until_complete(UserModel.objects.get(id=id))


# UserRequest 
@pytest.mark.userModel
@pytest.mark.userModelRequest
def test_model_user_request():
    attr: dict = case.valid_user
    user = UserRequest(**attr)

    assert [user.dict()[key] == value for key, value in attr.items()]
    assert check_password_hash(user.password, attr['password'])


# UserResponse
@pytest.mark.userModel
@pytest.mark.userModelResponse
def test_model_user_response():
    attr: dict = case.valid_user
    request = UserRequest(**attr)
    model = UserModel(**request.dict())
    model.id = 1
    response = UserResponse(**model.dict())
    
    assert [response.dict()[key] for key in model.dict() if key not in ['password', 'posts']]
