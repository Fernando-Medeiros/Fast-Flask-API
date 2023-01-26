from app.models.token import RefreshToken, Token
from app.models.user import UserModel
from app.security.backend import BackendDatabase
from app.security.session import authenticate_user, validate_credentials
from app.security.token import TokenJwt


class AuthController:
    backend = BackendDatabase

    @staticmethod
    async def token(form_data):
        user = await authenticate_user(
            form_data.username,
            form_data.password,
        )
        return Token(
            access_token=TokenJwt.create_access_token(
                sub=str(user.id),
                fresh=True,
            ),
            refresh_token=TokenJwt.create_refresh_token(
                sub=str(user.id),
            ),
        )

    @classmethod
    async def refresh_token(cls, token: str):
        _token = RefreshToken(refresh_token=token)

        data = validate_credentials(_token.refresh_token)

        user = await cls.backend.get_or_404(UserModel, id=int(data.sub))

        return Token(
            access_token=TokenJwt.create_access_token(
                sub=str(user.id),
                fresh=False,
            ),
            refresh_token=TokenJwt.create_refresh_token(
                sub=str(user.id),
            ),
        )
