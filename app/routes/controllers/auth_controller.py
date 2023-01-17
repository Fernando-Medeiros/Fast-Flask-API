from app.models.token import Token, TokenData
from app.models.user import UserModel

from ..security.login_required import (
    authenticate_user,
    get_user_or_404,
    validate_credentials,
)
from ..security.token_jwt import TokenJwt


async def token(form_data):
    user: UserModel = await authenticate_user(
        form_data.username,
        form_data.password,
    )
    return Token(
        access_token=TokenJwt.create_access_token(
            sub=user.username,
            fresh=True,
        ),
        refresh_token=TokenJwt.create_refresh_token(
            sub=user.username,
        ),
        token_type="bearer",
    )


async def refresh_token(form_data):
    data: TokenData = validate_credentials(form_data.refresh_token)
    user: UserModel = await get_user_or_404(username=data.username)
    return Token(
        access_token=TokenJwt.create_access_token(
            sub=user.username,
            fresh=False,
        ),
        refresh_token=TokenJwt.create_refresh_token(
            sub=user.username,
        ),
        token_type="bearer",
    )
