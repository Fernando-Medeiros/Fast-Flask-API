from typing import Any, Dict, Optional

from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: Optional[str | Dict],
        headers: Optional[Dict[str, Any]] = None,
    ):

        super().__init__(status_code, message, headers)


class BadRequest(BaseException):
    def __init__(self, message, headers: Optional[Dict[str, Any]] = None):
        return super().__init__(400, message, headers)


class Unauthorized(BaseException):
    def __init__(self, message, headers: Optional[Dict[str, Any]] = None):
        return super().__init__(401, message, headers)


class NotFound(BaseException):
    def __init__(self, message, headers: Optional[Dict[str, Any]] = None):
        return super().__init__(404, message, headers)


class InternalServerError(BaseException):
    def __init__(self, message, headers: Optional[Dict[str, Any]] = None):
        return super().__init__(500, message, headers)
