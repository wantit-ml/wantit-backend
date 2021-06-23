from json import dumps
from typing import Union, List, Optional

from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.db.vacancy import (
    create_vacancy,
    delete_vacancy,
    get_vacancies_by_user_id,
    get_vacancy_by_id,
)

router = APIRouter()


class VacancyModel(BaseModel):
    user_identifier: Union[int, str]
    title: str
    vacancy_code: str
    description: str
    stack: List[str]
    salary: int
    currency: str
    city: str
    address: str
    type_of_vacancy: str
    author: str
    phone: Optional[str]
    email: Optional[str]


@router.post("/create_vacancy_db")
async def create_vacancy_db(vacancy: VacancyModel):
    await create_vacancy(
        vacancy.user_identifier,
        vacancy.title,
        vacancy.vacancy_code,
        vacancy.description,
        vacancy.stack,
        vacancy.salary,
        vacancy.currency,
        vacancy.city,
        vacancy.address,
        vacancy.type_of_vacancy,
        vacancy.author,
        vacancy.phone,
        vacancy.email,
    )
    return Response(content="OK", status_code=200)


@router.get("/delete_vacancy_db")
async def delete_vacancy_db(vacancy_id: int):
    await delete_vacancy(vacancy_id)
    return Response(content="OK", media_type="plain/text", status_code=200)


@router.get("/get_by_user_id")
async def get_by_user_id(user_identifier: Union[int, str]):
    content = await get_vacancies_by_user_id(user_identifier)
    return Response(
        content=dumps(content),
        media_type="application/json",
        status_code=200,
    )


@router.get("/get_by_id")
async def get_by_id(vacancy_id: int):
    await get_vacancy_by_id(vacancy_id)
    return Response(content="OK", media_type="plain/text", status_code=200)
