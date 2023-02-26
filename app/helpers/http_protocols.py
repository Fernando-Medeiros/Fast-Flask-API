from fastapi import responses
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def StatusOk(content: str | dict | list | BaseModel | None) -> JSONResponse:
    return responses.JSONResponse(jsonable_encoder(content), 200)


def StatusCreated(content: str | dict | None) -> JSONResponse:
    return responses.JSONResponse(content, 201)


def StatusOkNoContent(content: str | dict | None) -> JSONResponse:
    return responses.JSONResponse(content, 204)
