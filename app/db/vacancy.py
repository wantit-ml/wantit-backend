from typing import List, Union, Optional
from app.db.db_setup import Vacancy, db
from app.db.user import get_user

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
	