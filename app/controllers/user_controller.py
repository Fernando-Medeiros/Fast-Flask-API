import base64
import os

import cloudinary.uploader

from app.helpers import BadRequest
from app.models import AccessModel, BirthdayModel, ProfileModel, UserModel
from app.repositories.backend import BackendDatabase
from app.requests import (
    RequestBirthday,
    RequestCreateAccount,
    UpdateAccount,
    UpdateAvatar,
    UpdateBackground,
    UpdateProfile,
)


class UserController:
    repository = BackendDatabase

    @classmethod
    async def get_all(cls) -> list[ProfileModel | None]:

        return await cls.repository.get_all_order_by(ProfileModel, "-id")

    @classmethod
    async def get_by_username(cls, username) -> ProfileModel:

        return await cls.repository.get_or_404(
            ProfileModel, "Username not found", username=username
        )

    @classmethod
    async def create_account(cls, request: RequestCreateAccount) -> None:

        data = request.dict(exclude={"username"}, exclude_none=True)

        if await cls.repository.get_or_none(UserModel, email=request.email):
            raise BadRequest("Email is already in use")

        if await cls.repository.get_or_none(ProfileModel, username=request.username):
            raise BadRequest("Username is already in use")

        account = await cls.repository.create_or_400(UserModel, **data)

        profile = await cls.repository.create_or_400(
            ProfileModel, account=account.pk, username=request.username
        )

        await cls.repository.create_or_400(AccessModel, user=profile.pk)

    @classmethod
    async def get_account_data(cls, current_user):

        return await current_user.load_all(True)

    @classmethod
    async def update_account(cls, request: UpdateAccount, current_user) -> None:
        data = request.dict(exclude_none=True)

        if not data:
            raise BadRequest("No content")

        if request.email and await cls.repository.get_or_none(
            UserModel, email=request.email
        ):
            raise BadRequest("Email is already in use")

        await current_user.account.update(**data)

    @classmethod
    async def upload_avatar(cls, image: str, current_user) -> None:

        data = UpdateAvatar(avatar=image).avatar

        if data is None:
            raise BadRequest("No content")

        try:
            bytes = base64.b64decode(data, validate=True)

            resp: dict = cloudinary.uploader.upload(
                bytes,
                width=500,
                height=500,
                crop="fill",
                folder=os.getenv("FOLDER_AVATAR"),
            )
        except Exception:
            raise BadRequest("Non-base64 digit found")
        else:
            await current_user.update(avatar=resp["url"])

    @classmethod
    async def upload_background(cls, image: str, current_user) -> None:

        data = UpdateBackground(background=image).background

        if data is None:
            raise BadRequest("No content")

        try:
            bytes = base64.b64decode(data, validate=True)

            resp: dict = cloudinary.uploader.upload(
                bytes,
                width=800,
                height=195,
                crop="fill",
                folder=os.getenv("FOLDER_BACKGROUND"),
            )
        except Exception:
            raise BadRequest("Non-base64 digit found")
        else:
            await current_user.update(background=resp["url"])

    @classmethod
    async def update_profile(cls, request: UpdateProfile, current_user) -> None:
        data = request.dict(exclude_none=True)

        if not data:
            raise BadRequest("No content")

        if await cls.repository.get_or_none(ProfileModel, username=request.username):
            raise BadRequest("Username is already in use")

        await current_user.update(**data)

    @classmethod
    async def update_birthday(cls, request: RequestBirthday, current_user) -> None:
        data = request.dict()

        result = await cls.repository.get_or_none(BirthdayModel, user=current_user.pk)

        if result:
            await result.update(**data)

        else:
            await cls.repository.create_or_400(
                BirthdayModel, user=current_user.pk, **data
            )

    @classmethod
    async def delete_account(cls, current_user) -> None:

        await cls.repository.delete_or_404(UserModel, id=current_user.id)
