from typing import Union
from app.db.db_setup import db, User, Firm
from app.db.user import get_user

async def create_firm(
	user_identifier: Union[int, str],
	title: str,
	phone: str,
	email: str,
	description: str,
	city: str,
	address: str
) -> None:
	user = await get_user(user_identifier)
	new_firm = Firm(title=title, phone=phone,
		email=email, description=description,
		city=city, address=address)
	user.firm.append(new_firm)
	db.commit()

