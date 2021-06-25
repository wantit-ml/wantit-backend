from typing import Union
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import Response, Cookie
from base64 import urlsafe_b64decode
from json import dumps
from app.db.user import get_matching_users
from app.db.vacancy import get_matching_vacancies
from app.auth.main import verify_cookie

router = APIRouter()


@router.get(
    "/get_matching_users",
    description="This method returns matching users for vacancy. Accepts vacancy id.",
)
async def fetch_matching_users(vacancy_id: int, session_cookie: str = Cookie(None)):
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    if await verify_cookie(username, session_id).role == "hr":
        raise HTTPException(status_code=403)
    matching_users_raw = await get_matching_users(vacancy_id)
    matching_users = list(map(lambda user: user.id, matching_users_raw))
    response = dumps(matching_users)
    return Response(content=response, media_type="application/json", status_code=200)


@router.get(
    "/get_matching_vacancies",
    description="This method returns matching vacancies for user. Accepts user indentifier",
)
async def fetch_matching_vacancies(user_identifier: Union[int, str], session_cookie: str = Cookie(None)):
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    await verify_cookie(username, session_id)
    matching_vacancies_raw = await get_matching_vacancies(user_identifier)
    matching_vacancies = list(
        map(lambda vacancy: vacancy.id, matching_vacancies_raw))
    response = dumps(matching_vacancies)
    return Response(content=response, media_type="application/json", status_code=200)
