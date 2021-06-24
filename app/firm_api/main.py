from ast import dump
from os import stat
from typing import Union
from json import dumps

from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Response

from app.db.firm import create_firm, get_firm_by_id, get_firm_by_user_id

router = APIRouter()


class CompanyModel(BaseModel):
    user_identifier: Union[int, str]
    title: str
    phone: str
    email: str
    description: str
    city: str
    address: str


@router.post("/create")
async def create_company(company: CompanyModel):
    await create_firm(
        company.user_identifier,
        company.title,
        company.phone,
        company.email,
        company.description,
        company.city,
        company.address,
    )
    return Response(content="OK", media_type="plain/text", status_code=200)


@router.get("/get_by_user")
async def get_company_by_user(user_identifier: Union[int, str]):
    company = await get_firm_by_user_id(user_identifier)
    json = dumps(
        {
            "id": company.id,
            "user_id": company.user_id,
            "title": company.title,
            "name": company.name,
            "surname": company.surname,
            "phone": company.phone,
            "email": company.email,
            "description": company.description,
            "logo": company.logo,
            "city": company.city,
            "address": company.address,
        }
    )
    return Response(content=json, media_type="application/json", status_code=200)


@router.get("/get_by_id")
async def get_company_by_id(company_id: int):
    company = await get_firm_by_id(company_id)
    json = dumps(
        {
            "id": company.id,
            "user_id": company.user_id,
            "title": company.title,
            "name": company.name,
            "surname": company.surname,
            "phone": company.phone,
            "email": company.email,
            "description": company.description,
            "logo": company.logo,
            "city": company.city,
            "address": company.address,
        }
    )
    return Response(content=json, media_type="application/json", status_code=200)