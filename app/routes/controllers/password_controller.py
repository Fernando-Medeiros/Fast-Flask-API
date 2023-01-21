from fastapi import HTTPException

from app.models.user import RecoverPassword, UpdatePassword, UserModel
from app.security.backend import BackendDatabase
from app.security.recovery_pwd import send_mail
from app.security.session import validate_credentials
from app.security.token import TokenJwt


class PwdController:
    backend = BackendDatabase

    @classmethod
    async def update_password(cls, password: str, current_user):
        data = UpdatePassword(password=password).dict()
        await current_user.account.update(**data)

        return {"detail": "Successfully updated password"}

    @classmethod
    async def recover_password(cls, email: str):
        data = RecoverPassword(email=email)

        user = await cls.backend.get_or_404(UserModel, email=data.email)

        send_mail(
            _email=user.email,
            TOKEN=TokenJwt.create_recover_token(sub=str(user.id)),
        )
        return {"detail": "Email sent, check your inbox"}

    @classmethod
    async def reset_password(cls, token: str, password: str, confirm: str):
        if password == confirm:
            hash_pwd = UpdatePassword(password=password).dict()

            payload = validate_credentials(token)

            user = await cls.backend.get_or_404(UserModel, id=int(payload.sub))

            await user.update(**hash_pwd)

            return {"detail": "Successfully updated password"}

        raise HTTPException(400, "Password and confirmation are different")
