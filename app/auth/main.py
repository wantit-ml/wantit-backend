from typing import Dict

from fastapi.routing import APIRouter
from fastapi import Response, status
from pydantic import BaseModel
from pydantic.tools import parse_raw_as

from app.db.user import create_user as create_user_in_db

router = APIRouter()


class UserRegistrationModel(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    role: str


class UserLoginModel(BaseModel):
    email: str
    password: str


@router.post(
    "/registration",
    responses={
        200: {
            "description": "Everything is OK",
            "content": {
                "text/plain": {
                    "example": "OK"
                }
            }
        },
        400: {
            "description": "Something went wrong",
            "content": {
                "text/plain": {
                    "example": "USERNAME_ALREADY_TAKEN"
                }
            }
        }
    }
)
async def create_user(user: UserRegistrationModel, response: Response):
    await create_user_in_db(
        user.username,
        user.password,
        user.email,
        user.phone,
        user.role
    )
    response.status_code = status.HTTP_200_OK
    return "OK"


@router.post(
    "/login",
    responses={
        200: {
            "description": "Everything is OK",
            "content": {
                "text/plain": {
                    "example": "OK"
                }
            }
        },
        401: {
            "description": "Authentication failed"
        }
    }
)
async def login_user(user: UserLoginModel, response: Response):
    if True:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    response.status_code = status.HTTP_200_OK
    return "OK"
    print(user)  # TODO: Login user
