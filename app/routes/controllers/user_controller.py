from datetime import datetime

from fastapi import status
from fastapi.exceptions import HTTPException

from app.models.user import UserModel

from ..security.login_required import verify_unique_constraint

model = UserModel


async def create_account(request_model):
    data = request_model.dict(exclude_unset=True)
    user = model(created_at=datetime.today(), **data)

    await verify_unique_constraint(
        model, "Username is already in use", username=user.username
    )
    await verify_unique_constraint(model, "Email is already in use", email=user.email)

    return await user.save()


async def get_all():
    return await model.objects.all()


async def get_by_username(username):
    entity = await model.objects.get_or_none(username=username)
    if entity:
        return entity

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")


async def get_account_data(current_user):
    return await model.objects.get(id=current_user.id)


async def update_user(request_model, current_user):
    entity = await model.objects.get(username=current_user.username)
    updates = request_model.dict(exclude_unset=True)
    return await entity.update(**updates)


async def update_password(request_model, current_user):
    entity = await model.objects.get(username=current_user.username)
    updates = request_model.dict(exclude_unset=True)
    await entity.update(**updates)

    return {"detail": "Successfully updated password"}


async def delete(current_user):

    if await model.objects.delete(username=current_user.username):
        return {"detail": "Account deleted"}

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User is not registered")
