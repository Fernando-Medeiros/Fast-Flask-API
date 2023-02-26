from app.repositories.backend import BackendDatabase
from app.responses import RefreshToken, Token
from app.security.session import authenticate_user, validate_credentials
from app.security.token import TokenJwt


class AuthController:
    repository = BackendDatabase

    @staticmethod
    async def token(form_data) -> Token:
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
    async def refresh_token(cls, token: str) -> Token:
        _token = RefreshToken(refresh_token=token)

        data = validate_credentials(_token.refresh_token)

        return Token(
            access_token=TokenJwt.create_access_token(
                sub=str(data.sub),
                fresh=False,
            ),
            refresh_token=TokenJwt.create_refresh_token(
                sub=str(data.sub),
            ),
        )
