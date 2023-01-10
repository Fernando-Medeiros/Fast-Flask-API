import asyncio
from datetime import datetime

import pytest
from fastapi import HTTPException
from werkzeug.security import check_password_hash

from app.models.user import (UserModel, UserRequest, UserRequestPatch,
                             UserRequestUpdatePassword, UserResponse,
                             UserResponseAccountData)
from tests.utils.user import CaseCreate

case = CaseCreate()


# UserModel - Valid
@pytest.mark.userModel
def test_model_valid_usermodel():
    data: dict = case.valid_user
    user = UserModel(**data)
    
    assert [user.dict()[key] for key in data]


# UserModel - Invalid
@pytest.mark.userModel
def test_model_invalid_user():
    with pytest.raises(HTTPException):
        attr: dict = case.invalid_user()
        user = UserModel(**attr)


# Save Account
@pytest.mark.userModel
def test_model_save_user():
    data: dict = case.valid_user
    user = UserModel(**data)
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
    data: dict = case.valid_user
    request = UserRequest(**data).dict()

    assert [request[key] for key in data]
    assert check_password_hash(str(request.get('password')), data['password'])


# UserRequestPatch
@pytest.mark.userModel
@pytest.mark.userModelRequest
def test_model_user_request_patch():
    data: dict = case.valid_user
    request = UserRequestPatch(**data).dict()

    assert [data[key] for key in request]


# UserRequestUpdatePassword
@pytest.mark.userModel
@pytest.mark.userModelRequest
def test_model_user_request_password():
    data: dict = case.valid_user
    request = UserRequestUpdatePassword(**data).dict()
    
    assert [data[key] for key in request]


# UserResponse
@pytest.mark.userModel
@pytest.mark.userModelResponse
def test_model_user_response():
    data: dict = case.valid_user.copy()
    data.update(id=1)
    response = UserResponse(**data).dict()
        
    assert [data[key] for key in response]
    

# UserResponseAccountData
@pytest.mark.userModel
@pytest.mark.userModelResponse
def test_model_user_response_account():
    data: dict = case.valid_user.copy()
    data.pop('password')
    data.update(id=1, created_at=datetime.today(), access=['user'])

    response = UserResponseAccountData(**data).dict()
        
    assert [response[key] for key in data]
