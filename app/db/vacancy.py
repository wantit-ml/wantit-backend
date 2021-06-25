from typing import List, Union, Optional
from app.db.db_setup import Vacancy, db
from app.db.user import get_user, get_about
from app.db.tags import get_languages, get_techs
from app.db.firm import get_firm_by_user_id, get_firm_by_id
from app.db.error_boundary import error_boundary
from app.ml.converter import Converter
from app.ml.match import MatchForUser


@error_boundary
async def create_vacancy(
    user_identifier: Union[int, str],
    title: str,
    vacancy_code: str,
    description: str,
    stack: List[str],
    foreign_languages: List[str],
    salary: int,
    currency: str,
    city: str,
    address: str,
    type_of_vacancy: str,
    author: str,
    phone: Optional[str],
    email: Optional[str],
) -> None:
    firm = await get_firm_by_user_id(user_identifier)
    if phone == None:
        phone = firm.phone
    if email == None:
        email = firm.email
    new_vacancy = Vacancy(
        title=title,
        vacancy_code=vacancy_code,
        description=description,
        stack=stack,
        salary=salary,
        currency=currency,
        city=city,
        foreign_languages=foreign_languages,
        address=address,
        type_of_vacancy=type_of_vacancy,
        author=author,
        phone=phone,
        email=email,
    )
    for tech in stack:
        try:
            new_tech = Tech(title=tech)
            db.add(new_tech)
        except:
            continue
    for language in foreign_languages:
        try:
            new_language = Language(title=language)
            db.add(new_language)
        except:
            continue
    firm.vacancies.append(new_vacancy)
    db.commit()
    await convert_vacancy(new_vacancy.id)


@error_boundary
async def delete_vacancy(vacancy_id: int) -> None:
    db.query(Vacancy).filter(Vacancy.id == vacancy_id).delete(
        synchronize_session="fetch"
    )
    db.commit()


async def get_vacancies_by_user_id(user_identifier: Union[int, str]) -> List[Vacancy]:
    user = await get_user(user_identifier)
    firm = user.firm[0]
    vacancies = firm.vacancies
    return vacancies


async def get_vacancy_by_id(vacancy_id: int) -> Vacancy:
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).one()
    return vacancy


@error_boundary
async def convert_vacancy(vacancy_id: int) -> None:
    vacancy = await get_vacancy_by_id(vacancy_id)
    techs = await get_techs()
    languages = await get_languages()
    converter = Converter(techs, languages)
    code = await converter.convert(vacancy)
    vacancy.code = code
    db.commit()


async def get_matching_vacancies(user_identifier: Union[int, str]) -> List[Vacancy]:
    about = await get_about(user_identifier)
    vacancies = db.query(Vacancy).all()
    matching_vacancies_ids = await MatchForUser.search_vacancies(about, vacancies)
    matching_vacancies = []
    for vacancy in vacancies:
        if vacancy.id in matching_vacancies_ids:
            matching_vacancies.append(vacancy)
    return matching_vacancies


async def get_vacancies_by_firm(firm_id: int) -> List[Vacancy]:
    firm = get_firm_by_id(firm_id)
    return firm.vacancies

async def get_all_vacancies() -> List[Vacancy]:
    vacancies = db.query(Vacancy).all()
    return vacancies
