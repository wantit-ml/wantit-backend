from typing import Union, List, Dict
from datetime import datetime

from fastapi.routing import APIRouter
from pydantic import BaseModel
from fastapi import Response, status

from app.db.user import create_about

router = APIRouter()


class UserAboutModel(BaseModel):
    identifier: Union[int, str]
    name: str
    surname: str
    city: str
    birthday: datetime
    gender: str
    citizenships: List[str]
    rank: str
    salary: int
    currency: str
    stack: List[str]
    school: str
    grade: int
    native_language: str
    foreign_languages: List[str]
    can_move: str
    metro_station: str
    github_id: str
    vk_id: str
    telegram_id: str
    timetable: List[Dict]
    achievements: List[Dict]


@router.post('/fill_about')
async def fill_about(user: UserAboutModel):
    print(user)
    await create_about(
        user.identifier,
        user.name,
        user.surname,
        user.city,
        user.birthday,
        user.gender,
        user.citizenships,
        user.rank,
        user.salary,
        user.currency,
        user.stack,
        user.school,
        user.grade,
        user.native_language,
        user.foreign_languages,
        user.can_move,
        user.metro_station,
        user.github_id,
        user.vk_id,
        user.telegram_id,
        user.timetable,
        user.achievements
    )
    return Response(status_code=200)
