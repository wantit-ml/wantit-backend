from os import sep, stat
from typing import Union, List, Dict
from datetime import datetime
from json import dumps
from fastapi.exceptions import HTTPException

from fastapi.routing import APIRouter
from pydantic import BaseModel
from fastapi import Response, Cookie
from starlette.requests import Request

from app.db.user import create_about, get_about
from app.auth.main import verify_cookie

router = APIRouter()


class UserAboutModel(BaseModel):
    identifier: Union[int, str]
    name: str
    surname: str
    description: str
    city: str
    birthday: datetime
    gender: str
    citizenships: List[str]
    rank: str
    salary: int
    currency: str
    stack: List[str]
    school: str
    age: int
    native_language: str
    foreign_languages: List[str]
    can_move: str
    metro_station: str
    github_id: str
    vk_id: str
    telegram_id: str
    timetable: List[Dict]
    achievements: List[Dict]


@router.post("/fill_about")
async def fill_about(user: UserAboutModel, session_cookie: str = Cookie(None)):
    username, session_id = session_cookie.split(":")
    session_user = await verify_cookie(username, session_id)
    if user.identifier.isnumeric() and (not session_user.id == user.identifier):
        raise HTTPException(status_code=403)
    elif not session_user.username == user.identifier:
        raise HTTPException(status_code=403)
    await create_about(
        user.identifier,
        user.name,
        user.surname,
        user.description,
        user.city,
        user.birthday,
        user.gender,
        user.citizenships,
        user.rank,
        user.salary,
        user.currency,
        user.stack,
        user.school,
        user.age,
        user.native_language,
        user.foreign_languages,
        user.can_move,
        user.metro_station,
        user.github_id,
        user.vk_id,
        user.telegram_id,
        user.timetable,
        user.achievements,
    )
    return Response(status_code=200)


@router.get(
    "/get_about",
    description="This method returns user's about page. Accepts id or username.",
)
async def fetch_about(identifier: Union[str, int] = None, session_cookie: str = Cookie(None)):
    username, session_id = session_cookie.split(":")
    await verify_cookie(username, session_id)
    about = await get_about(identifier)
    timetable = [{"day": entry.day, "time": entry.time}
                 for entry in about.timetable]
    response = dumps(
        {
            "user_id": about.user_id,
            "name": about.name,
            "surname": about.surname,
            "description": about.description,
            "city": about.city,
            "birthday": about.birthday.strftime("%a,%d %b %Y %H:%M:%S"),
            "gender": about.gender,
            "citizenships": about.citizenships,
            "rank": about.rank,
            "salary": about.salary,
            "currency": about.currency,
            "stack": about.stack,
            "school": about.school,
            "age": about.age,
            "native_language": about.native_language,
            "foreign_languages": about.foreign_languages,
            "can_move": about.can_move,
            "metro_station": about.metro_station,
            "timetable": timetable,
            "github_id": about.github_id,
            "vk_id": about.vk_id,
            "telegram_id": about.telegram_id,
        }
    )
    return Response(content=response, media_type="application/json", status_code=200)
