from typing import List, Union, Optional
from app.db.db_setup import Vacancy, db
from app.db.user import get_user
from app.db.tags import get_languages, get_techs
from app.ml.converter import Converter

async def create_vacancy(
	user_identifier: Union[int, str],
	title: str,
	vacancy_code: str,
	description: str,
	stack: List[str],
	salary: int, 
	currency: str,
	city: str,
	address: str,
	type_of_vacancy: str,
	author: str,
	phone: Optional[str],
	email: Optional[str],
) -> None:
	user = await get_user(user_identifier)
	firm = user.firm[0]
	if phone == None:
		phone = firm.phone
	if email == None:
		email = firm.email
	new_vacancy = Vacancy(title=title, vacancy_code=vacancy_code,
		description=description, stack=stack,
		salary=salary, currency=currency,
		city=city, address=address,
		type_of_vacancy=type_of_vacancy, author=author,
		phone=phone, email=email)
	firm.vacancies.append(new_vacancy)
	db.commit()

async def delete_vacancy(vacancy_id: int) -> None:
	db.query(Vacancy).filter(Vacancy.id == vacancy_id).delete(
		synchronize_session="fetch")
	db.commit()


async def get_vacancies_by_user_id(user_identifier: Union[int, str]) -> List(Vacancy):
	user = await get_user(user_identifier)
	firm = user.firm[0]
	vacancies = firm.vacancies
	return vacancies

async def get_vacancy_by_id(vacancy_id: int) -> Vacancy:
	vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).one()
	return vacancy

async def convert_vacancy(vacancy_id: int) -> None:
	vacancy = await get_vacancy_by_id(vacancy_id)
	techs = await get_techs()
	languages = await get_languages()
	converter = Converter(techs, languages)
	code = await converter.convert(vacancy)
	vacancy.code = code
	db.commit()