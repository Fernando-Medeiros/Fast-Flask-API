from fastapi import HTTPException

from app.models.user import RequestRecoverPassword, RequestUpdatePassword, UserModel

from ..security.login_required import get_user_or_404, validate_credentials
from ..security.send_recovery_email import send_mail
from ..security.token_jwt import TokenJwt


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

        user: UserModel = await get_user_or_404(username=payload.username)

        await user.update(**hash_pwd.dict())

        return {"detail": "Successfully updated password"}

    raise HTTPException(
        status_code=400, detail="Password and confirmation are different"
    )
