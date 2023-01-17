from typing import List

from fastapi import APIRouter, Depends, Form

from app.models.user import (
    RequestRecoverPassword,
    RequestUpdate,
    RequestUpdatePassword,
    UserModel,
    UserRequest,
    UserResponse,
    UserResponseAccountData,
)

from .controllers import user_controller
from .security.login_required import login_required

users = APIRouter()
password = APIRouter()


# PULIC ROUTES
@users.get("", response_model=List[UserResponse])
async def get_list_with_all_users():

    return await user_controller.get_all_users()


@users.get("/{username}", response_model=UserResponse)
async def get_by_username(username: str):

    return await user_controller.get_by_username(username)


@users.post("", response_model=UserResponse, status_code=201)
async def new_account(request_model: UserRequest):

    return await user_controller.create_account(request_model)


# PRIVATE ROUTES
@users.patch("/update")
async def update_account(
    request_model: RequestUpdate, current_user: UserModel = Depends(login_required)
):
    return await user_controller.update_account(request_model, current_user)


@users.delete("/delete")
async def delete_account(current_user: UserModel = Depends(login_required)):

    return await user_controller.delete_account(current_user)


@users.get("/account/", response_model=UserResponseAccountData)
async def get_account_data(current_user: UserModel = Depends(login_required)):

    return await user_controller.get_account_data(current_user)


# PASSWORD ROUTES
@password.post("/password/recover")
async def recover_password(request_model: RequestRecoverPassword):

    return await user_controller.recover_password(request_model)


@password.patch("/password/reset/{token}")
async def reset_password(
    token: str, password: str = Form(...), confirm: str = Form(...)
):

    return await user_controller.reset_password(token, password, confirm)


@password.patch("/password/update")
async def update_password(
    request_model: RequestUpdatePassword,
    current_user: UserModel = Depends(login_required),
):
    return await user_controller.update_password(request_model, current_user)
