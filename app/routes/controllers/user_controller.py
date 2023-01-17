from datetime import datetime

from app.models.user import RequestUpdate, UserModel, UserRequest

from ..security.login_required import get_user_or_404, verify_unique_constraint

model = UserModel


async def create_account(request_model: UserRequest):
    data = request_model.dict(exclude_unset=True)
    user = UserModel(created_at=datetime.today(), **data)

    await verify_unique_constraint(
        model,
        "Username is already in use",
        username=user.username,
    )
    await verify_unique_constraint(
        model,
        "Email is already in use",
        email=user.email,
    )
    return await user.save()


async def get_all_users():
    return await model.objects.all()


async def get_by_username(username: str):
    return await get_user_or_404(username=username)


async def get_account_data(current_user: UserModel):
    return await model.objects.get(id=current_user.id)


async def update_account(request_model: RequestUpdate, current_user: UserModel):
    user = await get_user_or_404(username=current_user.username)
    updates = request_model.dict(exclude_unset=True)

    await user.update(**updates)

    return {"detail": "The data has been updated"}


async def delete_account(current_user: UserModel):
    result: int = await model.objects.delete(username=current_user.username)
    if result or result is None:
        return {"detail": "Account deleted"}
