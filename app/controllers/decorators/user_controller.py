from datetime import datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from ...models.user import UserModel

model = UserModel


async def create_account(request_model):
    data = request_model.dict(exclude_unset=True)
    entity = model(created_at=datetime.today(), **data)

    unique_username = await model.objects.get_or_none(username=data["username"])
    unique_email = await model.objects.get_or_none(email=data["email"])

    if unique_username:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Username is already in use"
        )
    elif unique_email:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Email is already in use"
        )
    return await entity.save()


async def get_all():
    return await model.objects.all()


async def get_by_username(username):
    entity = await model.objects.get_or_none(username=username)
    if entity:
        return entity

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Not Found")


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

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Successfully updated password",
    }


async def delete(current_user):
    if await model.objects.delete(username=current_user.username):
        return {"status_code": status.HTTP_200_OK, "detail": "Account deleted"}
