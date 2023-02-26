from typing import List

from fastapi import APIRouter, Depends, Form

from app.controllers import UserController
from app.helpers import StatusCreated, StatusOk, StatusOkNoContent
from app.models import ProfileModel
from app.requests import (
    RequestBirthday,
    RequestCreateAccount,
    UpdateAccount,
    UpdateProfile,
)
from app.responses import AccountResponse, ProfileResponse
from app.security.session import session

router = APIRouter()


# PUBLIC ROUTES
@router.get("", response_model=List[ProfileResponse])
async def get_list_with_all_profiles():
    resp = await UserController.get_all()

    return StatusOk(resp)


@router.get("/{username}", response_model=ProfileResponse)
async def get_profile_by_username(username: str):
    resp = await UserController.get_by_username(username)

    return StatusOk(resp)


@router.post("")
async def create_new_account(request: RequestCreateAccount):
    resp = await UserController.create_account(request)

    return StatusCreated(resp)


# PRIVATE ROUTES
@router.get("/account/", response_model=AccountResponse)
async def get_account_data(current_user: ProfileModel = Depends(session)):
    resp = await UserController.get_account_data(current_user)

    return StatusOk(resp)


@router.patch("/account")
async def update_account(
    request: UpdateAccount,
    current_user: ProfileModel = Depends(session),
):
    resp = await UserController.update_account(request, current_user)

    return StatusOkNoContent(resp)


@router.patch("/profile")
async def update_profile(
    request: UpdateProfile,
    current_user: ProfileModel = Depends(session),
):
    resp = await UserController.update_profile(request, current_user)

    return StatusOkNoContent(resp)


@router.patch("/avatar")
async def upload_avatar(
    image: str = Form(...),
    current_user: ProfileModel = Depends(session),
):
    resp = await UserController.upload_avatar(image, current_user)

    return StatusOkNoContent(resp)


@router.patch("/background")
async def upload_background(
    image: str = Form(...),
    current_user: ProfileModel = Depends(session),
):
    resp = await UserController.upload_background(image, current_user)

    return StatusOkNoContent(resp)


@router.put("/birthday")
async def update_birthday(
    request: RequestBirthday,
    current_user: ProfileModel = Depends(session),
):
    resp = await UserController.update_birthday(request, current_user)

    return StatusOkNoContent(resp)


@router.delete("")
async def delete_account(current_user: ProfileModel = Depends(session)):
    resp = await UserController.delete_account(current_user)

    return StatusOkNoContent(resp)
