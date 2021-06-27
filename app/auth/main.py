from typing import Dict, Union
from json import dumps
from fastapi.params import Cookie
from base64 import urlsafe_b64encode, urlsafe_b64decode

from fastapi.routing import APIRouter
from fastapi import Response, status, Depends, HTTPException
from pydantic import BaseModel

from app.db.user import (
    create_user as create_user_in_db,
    create_session,
    UserAlreadyExists,
    WrongPassword,
    get_user,
    verify_session,
    expire_session
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
    role: str


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


@router.post("/login")
async def get_session(user: UserLoginModel):
    user_info = await get_user(user.username)
    if not user_info.role == user.role:
        raise HTTPException(status_code=400, detail="Wrong role.")
    try:
        session_id = await create_session(user.username, user.password)
    except WrongPassword:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    json = dumps(
        {
            "id": user_info.id,
            "username": user_info.username,
            "email": user_info.email,
            "phone": user_info.phone,
            "role": user_info.role
        }
    )
    response = Response(
        content=json,
        headers={"Content-Type": "application/json"},
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="session_cookie", value=urlsafe_b64encode((user.username + ":" + session_id).encode()).decode(), httponly=True, samesite="None", secure=True
    )
    return response


@router.get("/logout")
async def logout(session_cookie: str = Cookie(None)):
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    session_user = await verify_cookie(username, session_id)
    if not session_user.username == username:
        raise HTTPException(status_code=401)
    await expire_session(session_id)
    return Response(status_code=200)


async def verify_cookie(username: str, session_id: str):
    credentials_exception = HTTPException(
        status_code=401, detail="Couldn't validate credentials"
    )
    user = await verify_session(username, session_id)
    if user is None:
        raise credentials_exception
    else:
        return user
