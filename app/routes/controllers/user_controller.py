from fastapi import HTTPException

from app.models.user import (
    AccessModel,
    BirthdayModel,
    ProfileModel,
    RequestBirthday,
    RequestCreateAccount,
    UpdateAccount,
    UpdateAvatar,
    UpdateBirthday,
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

        if await cls.backend.get_or_none(UserModel, email=request.email):
            raise HTTPException(404, "Email is already in use")

        await current_user.account.update(**data)

        return {"detail": "The data has been updated"}

    @classmethod
    async def update_avatar(cls, request: UpdateAvatar, current_user):
        data = request.dict(exclude_none=True)

        if not data:
            raise HTTPException(400, "No content")

        await current_user.update(**data)

        return {"detail": "The data has been updated"}

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
    async def insert_birthday(cls, request: RequestBirthday, current_user):
        data = request.dict(exclude_none=True)
        await cls.backend.create_or_400(BirthdayModel, user=current_user.pk, **data)

        return {"detail": "The data has been updated"}

    @classmethod
    async def update_birthday(cls, request: UpdateBirthday, current_user):
        data = request.dict(exclude_none=True)

        if not data:
            raise HTTPException(400, "No content")

        model = await cls.backend.get_or_404(BirthdayModel, id=current_user.id)

        await model.update(**data)

        return {"detail": "The data has been updated"}

    @classmethod
    async def delete_account(cls, current_user):
        await cls.backend.delete_or_404(UserModel, id=current_user.id)

        return {"detail": "Account deleted"}
