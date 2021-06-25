from typing import Dict, Union
from fastapi.params import Cookie

from fastapi.routing import APIRouter
from fastapi import Response, status, Depends, HTTPException
from pydantic import BaseModel

from app.db.user import (
    create_user as create_user_in_db,
    create_session,
    UserAlreadyExists,
    WrongPassword,
    verify_session,
)

router = APIRouter()


class UserRegistrationModel(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    role: str


class UserLoginModel(BaseModel):
    username: str
    password: str


@router.post(
    "/registration",
    responses={
        200: {
            "description": "Everything is OK",
            "content": {"text/plain": {"example": "OK"}},
        },
        400: {
            "description": "Something went wrong",
            "content": {"text/plain": {"example": "USERNAME_ALREADY_TAKEN"}},
        },
    },
)
async def create_user(user: UserRegistrationModel):
    try:
        await create_user_in_db(
            user.username, user.password, user.email, user.phone, user.role
        )
    except UserAlreadyExists:
        return Response(
            content="USERNAME_ALREADY_TAKEN",
            headers={"Content-Type": "text/plain"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        content="OK",
        headers={"Content-Type": "text/plain"},
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/login",
    responses={
        200: {
            "description": "Everything is OK",
            "content": {"text/plain": {"example": "OK"}},
        },
        401: {
            "description": "Auth failed",
            "content": {"text/plain": {"example": "WRONG_PASSWORD"}},
        },
    },
)
async def get_session(user: UserLoginModel):
    try:
        session_id = await create_session(user.username, user.password)
    except WrongPassword:
        return Response(
            content="WRONG_PASSWORD",
            headers={"Content-Type": "text/plain"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    response = Response(
        content="OK",
        headers={"Content-Type": "text/plain"},
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="session_cookie", value=user.username + ":" + str(session_id), httponly=True
    )
    return response


async def verify_cookie(session_cookie: Cookie = Depends()):
    username, session_id = session_cookie.split(":")
    credentials_exception = HTTPException(
        status_code=401, detail="Couldn't validate credentials"
    )
    if not await verify_session(username, session_id):
        raise credentials_exception
    else:
        return None
