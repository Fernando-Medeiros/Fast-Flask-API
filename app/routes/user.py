from typing import List

from fastapi import APIRouter, Depends, Form

from app.models.user import (
    AccountDataResponse,
    ProfileModel,
    ProfileResponse,
    RequestBirthday,
    RequestCreateAccount,
    UpdateAccount,
    UpdateProfile,
)
from app.security.session import session

from .controllers.user_controller import UserController

router = APIRouter()


# PULIC ROUTES
@router.get("", response_model=List[ProfileResponse])
async def get_list_with_all_profiles():

    return await UserController.get_all()


@router.get("/{username}", response_model=ProfileResponse)
async def get_profile_by_username(username: str):

    return await UserController.get_by_username(username)


@router.post("", status_code=201)
async def create_new_account(request: RequestCreateAccount):

    return await UserController.create_account(request)


# PRIVATE ROUTES
@router.get("/account/", response_model=AccountDataResponse)
async def get_account_data(current_user: ProfileModel = Depends(session)):

    return await UserController.get_account_data(current_user)


@router.patch("/account")
async def update_account(
    request: UpdateAccount,
    current_user: ProfileModel = Depends(session),
):
    return await UserController.update_account(request, current_user)


@router.patch("/profile")
async def update_profile(
    request: UpdateProfile,
    current_user: ProfileModel = Depends(session),
):
    return await UserController.update_profile(request, current_user)


@router.patch("/avatar")
async def upload_avatar(
    image: str = Form(...),
    current_user: ProfileModel = Depends(session),
):
    return await UserController.upload_avatar(image, current_user)


@router.patch("/background")
async def upload_background(
    image: str = Form(...),
    current_user: ProfileModel = Depends(session),
):
    return await UserController.upload_background(image, current_user)


@router.put("/birthday")
async def update_birthday(
    request: RequestBirthday,
    current_user: ProfileModel = Depends(session),
):
    return await UserController.update_birthday(request, current_user)


@router.delete("")
async def delete_account(current_user: ProfileModel = Depends(session)):

    return await UserController.delete_account(current_user)
