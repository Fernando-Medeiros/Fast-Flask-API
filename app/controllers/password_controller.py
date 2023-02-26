from app.helpers import BadRequest
from app.models.user import UserModel
from app.repositories.backend import BackendDatabase
from app.requests import RecoverPassword, UpdatePassword
from app.security.recovery import send_mail
from app.security.session import validate_credentials
from app.security.token import TokenJwt


class PwdController:
    repository = BackendDatabase

    @classmethod
    async def update_password(cls, password: str, current_user) -> None:
        data = UpdatePassword(password=password).dict()

        await current_user.account.update(**data)

    @classmethod
    async def recover_password(cls, email: str) -> dict[str, str]:
        data = RecoverPassword(email=email)

        user = await cls.repository.get_or_404(UserModel, email=data.email)

        send_mail(
            _email=user.email,
            TOKEN=TokenJwt.create_recover_token(sub=str(user.id)),
        )
        return {"detail": "Email sent, check your inbox"}

    @classmethod
    async def reset_password(cls, token: str, password: str, confirm: str) -> None:
        if password == confirm:
            hash_pwd = UpdatePassword(password=password).dict()

            payload = validate_credentials(token)

            user = await cls.repository.get_or_404(UserModel, id=int(payload.sub))

            await user.update(**hash_pwd)

            return

        raise BadRequest("Password and confirmation are different")
