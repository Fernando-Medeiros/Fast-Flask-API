import ormar
from jose import JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..models.token import TokenData
from ..models.user import UserModel
from .token_jwt import DecodeTokenJwt


class AuthBearer:
    url: str = '/auth/token'
    auth_scheme = OAuth2PasswordBearer(tokenUrl=url)


class ValidateCredentials:
    def validate(self, token: str) -> TokenData:
        try:
            payload: dict = DecodeTokenJwt().decode(token)
            return TokenData(**payload)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


class ValidateUser:
    model: ormar.Model = UserModel
    
    async def get_or_none(self, payload) -> UserModel:
        user = await self.model.objects.get_or_none(id=payload.id)
        
        if user == None:
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )
        return user


async def request_token(token: str = Depends(AuthBearer.auth_scheme)) -> UserModel:
    payload = ValidateCredentials().validate(token) 
    user = await ValidateUser().get_or_none(payload)
    return user


async def login_required(current_user: UserModel = Depends(request_token)):
    return current_user