from datetime import datetime

from fastapi import HTTPException

from app.models.user import (
    RequestRecoverPassword,
    RequestUpdate,
    RequestUpdatePassword,
    UserModel,
    UserRequest,
)

from ..security.login_required import (
    get_user_or_404,
    validate_credentials,
    verify_unique_constraint,
)
from ..security.send_recovery_email import send_mail
from ..security.token_jwt import TokenJwt

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


# PASSWORD
async def update_password(
    request_model: RequestUpdatePassword, current_user: UserModel
):
    user = await get_user_or_404(username=current_user.username)
    updates = request_model.dict(exclude_unset=True)

    await user.update(**updates)

    return {"detail": "Successfully updated password"}


async def recover_password(request_model: RequestRecoverPassword):
    user = await get_user_or_404(
        email=request_model.email,
        bday=request_model.bday,
    )
    send_mail(
        _email=user.email,
        TOKEN=TokenJwt.create_recover_token(sub=user.username),
    )
    return {"detail": "Email sent, check your inbox"}


async def reset_password(token: str, password: str, confirm: str):
    if password == confirm:
        hash_pwd = RequestUpdatePassword(password=password)

        payload = validate_credentials(token)

        user = await get_user_or_404(username=payload.username)

        await user.update(**hash_pwd.dict())

        return {"detail": "Successfully updated password"}

    raise HTTPException(
        status_code=404, detail="Password and confirmation are different"
    )
