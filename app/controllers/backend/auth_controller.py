from fastapi import HTTPException, status
from werkzeug.security import check_password_hash

from app.utils.token_jwt import CreateTokenJwt


async def post_token(model, form_data):
    entity = await model.objects.get_or_none(email=form_data.username)

    if not entity or not check_password_hash(entity.password, form_data.password):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="User not found or invalid password",
        )
    return {
        "access_token": CreateTokenJwt().create_token(id=entity.id),
        "token_type": "bearer",
    }
