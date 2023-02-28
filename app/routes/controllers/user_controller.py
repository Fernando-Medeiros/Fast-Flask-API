import base64
import os

import cloudinary.uploader
from fastapi import HTTPException

from app.models.user import (
    AccessModel,
    BirthdayModel,
    ProfileModel,
    RequestBirthday,
    RequestCreateAccount,
    UpdateAccount,
    UpdateAvatar,
    UpdateBackground,
    UpdateProfile,
    UserModel,
)
from app.security.backend import BackendDatabase


class UserController:
    backend = BackendDatabase

    @classmethod
    async def get_all(cls):
        return await cls.backend.get_all_order_by(ProfileModel, "-id")

    @classmethod
    async def get_by_username(cls, username):
        return await cls.backend.get_or_404(ProfileModel, username=username)

    @classmethod
    async def create_account(cls, request: RequestCreateAccount):
        data = request.dict(exclude={"username"}, exclude_none=True)

        if await cls.backend.get_or_none(UserModel, email=request.email):
            raise HTTPException(400, "Email is already in use")

        if await cls.backend.get_or_none(ProfileModel, username=request.username):
            raise HTTPException(400, "Username is already in use")

        account = await cls.backend.create_or_400(UserModel, **data)

        profile = await cls.backend.create_or_400(
            ProfileModel, account=account.pk, username=request.username
        )
        await cls.backend.create_or_400(AccessModel, user=profile.pk)

        return {"detail": "Account created successfully"}

    @classmethod
    async def get_account_data(cls, current_user):
        return await current_user.load_all(True)

    @classmethod
    async def update_account(cls, request: UpdateAccount, current_user):
        data = request.dict(exclude_none=True)

        if not data:
            raise HTTPException(400, "No content")

        if request.email and await cls.backend.get_or_none(
            UserModel, email=request.email
        ):
            raise HTTPException(400, "Email is already in use")

        await current_user.account.update(**data)

        return {"detail": f"The {', '.join(data.keys())} has been updated"}

    @classmethod
    async def upload_avatar(cls, image: str, current_user):

        data = UpdateAvatar(avatar=image).avatar

        if data is None:
            raise HTTPException(400, "No content")

        try:
            bytes = base64.b64decode(data, validate=True)

            resp: dict = cloudinary.uploader.upload(
                bytes,
                width=500,
                height=500,
                crop="fill",
                folder=os.getenv("FOLDER_AVATAR"),
            )
        except:
            raise HTTPException(400, "Non-base64 digit found")
        else:
            await current_user.update(avatar=resp["url"])

            return {"detail": "The avatar has been updated"}

    @classmethod
    async def upload_background(cls, image: str, current_user):

        data = UpdateBackground(background=image).background

        if data is None:
            raise HTTPException(400, "No content")

        try:
            bytes = base64.b64decode(data, validate=True)

            resp: dict = cloudinary.uploader.upload(
                bytes,
                width=800,
                height=195,
                crop="fill",
                folder=os.getenv("FOLDER_BACKGROUND"),
            )
        except:
            raise HTTPException(400, "Non-base64 digit found")
        else:
            await current_user.update(background=resp["url"])

            return {"detail": "The background has been updated"}

    @classmethod
    async def update_profile(cls, request: UpdateProfile, current_user):
        data = request.dict(exclude_none=True)

        if not data:
            raise HTTPException(400, "No content")

        if await cls.backend.get_or_none(ProfileModel, username=request.username):
            raise HTTPException(404, "Username is already in use")

        await current_user.update(**data)

        return {"detail": "The data has been updated"}

    @classmethod
    async def update_birthday(cls, request: RequestBirthday, current_user):
        data = request.dict()

        result = await cls.backend.get_or_none(BirthdayModel, user=current_user.pk)

        if result:
            await result.update(**data)

        else:
            await cls.backend.create_or_400(BirthdayModel, user=current_user.pk, **data)

        return {"detail": "The birthday has been updated"}

    @classmethod
    async def delete_account(cls, current_user):
        await cls.backend.delete_or_404(UserModel, id=current_user.id)

        return {"detail": "Account deleted"}
