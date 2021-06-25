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

async def get_firm_by_user_id(user_identifier: Union[int, str]) -> Firm:
    user = await get_user(user_identifier)
    return user.firm[0]

async def get_firm_by_id(firm_id: int) -> Firm:
    firm = db.query(Firm).filter(Firm.id == firm_id).one()
    return firm

