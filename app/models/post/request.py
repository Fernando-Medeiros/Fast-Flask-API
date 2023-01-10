import re

from pydantic import BaseModel, validator

from fastapi import HTTPException, status


class PostRequest(BaseModel):
    content: str

    @validator('content')
    def _content(cls, value):
        
        if not re.compile(r'^([A-Za-z0-9]).{3,}$').match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid content!'
            )
        return value


class PostRequestPatch(BaseModel):
    content: str

    @validator('content')
    def _content(cls, value):
        
        if not re.compile(r'^([A-Za-z0-9]).{3,}$').match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid content!'
            )
        return value