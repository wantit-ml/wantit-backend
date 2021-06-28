from typing import List

from app.db.db_setup import About, Vacancy
from os import stat
from typing import Union
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import Response, Cookie
from base64 import urlsafe_b64decode
from json import dumps

from starlette import status
from app.db import vacancy
from app.db.user import get_about, get_matching_users
from app.db.vacancy import get_matching_vacancies, get_vacancies_by_user_id
from app.auth.main import verify_cookie

router = APIRouter()


@router.get(
    "/get_matching_users",
    description="This method returns matching users for vacancy. Accepts vacancy id.",
)
async def fetch_matching_users(vacancy_id: int, session_cookie: str = Cookie(None)):
    if session_cookie is None:
        raise HTTPException(status_code=400, detail="Cookie is empty")
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    user = await verify_cookie(username, session_id)
    if user.role != "hr":
        raise HTTPException(status_code=403)
    matching_users_raw = await get_matching_users(vacancy_id)
    response = dumps([
        {
            "id": item.id,
            "username": item.username,
            "email": item.email,
            "phone": item.phone,
            "role": item.role
        } for item in matching_users_raw
    ])
    return Response(content=response, media_type="application/json", status_code=200)


@router.get("/get_matching_users_for_all_vacancies")
async def fetch_all_matching_users(session_cookie: str = Cookie(None)):
    if session_cookie is None:
        raise HTTPException(status_code=400, detail="Cookie is empty")
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    user = await verify_cookie(username, session_id)
    if not user.role == "hr":
        raise HTTPException(status_code=403)
    vacancies: List[Vacancy] = await get_vacancies_by_user_id(user.id)
    matching_users = []
    for vacancy in vacancies:
        matching_users_raw = await get_matching_users(vacancy.id)
        for item_user in matching_users_raw:
            about = await get_about(item_user.id)
            matching_users.append({
                "id": item_user.id,
                "username": item_user.username,
                "email": item_user.email,
                "phone": item_user.phone,
                "name": about.name,
                "surname": about.surname,
                "city": about.city,
                "gender": about.gender,
                "rank": about.rank,
                "currency": about.currency,
                "salary": about.salary,
                "school": about.school,
                "age": about.age,
                "can_move": about.can_move,
                "stack": about.stack
            })
    print(matching_users)
    return Response(content=dumps(matching_users), status_code=200)


@router.get(
    "/get_matching_vacancies",
    description="This method returns matching vacancies for user. Accepts user indentifier",
)
async def fetch_matching_vacancies(user_identifier: Union[int, str], session_cookie: str = Cookie(None)):
    if session_cookie is None:
        raise HTTPException(status_code=400, detail="Cookie is empty.find()")
    username, session_id = urlsafe_b64decode(
        session_cookie).decode().split(":")
    await verify_cookie(username, session_id)
    vacancies = await get_matching_vacancies(user_identifier)
    json = dumps([
        {
            "id": vacancy.id,
            "title": vacancy.title,
            "vacancy_code": vacancy.vacancy_code,
            "description": vacancy.description,
            "stack": vacancy.stack,
            "salary": vacancy.salary,
            "currency": vacancy.currency,
            "city": vacancy.city,
            "address": vacancy.address,
            "type_of_vacancy": vacancy.type_of_vacancy,
            "author": vacancy.author,
            "phone": vacancy.phone,
            "email": vacancy.email,
            "code": vacancy.code,
        }
        for vacancy in vacancies
    ])
    return Response(content=json, media_type="application/json", status_code=200)
