from typing import Union
from app.db.db_setup import db, User, Salt
import hashlib
import bcrypt

async def create_user(username: str, password_raw: str, email: str, phone: str, role: str) -> None:
	salt = bcrypt.gensalt()
	hash_object = hashlib.sha256(password_raw.encode() + salt)
	password = hash_object.hexdigest()
	new_salt = Salt(salt=salt)
	new_user = User(username=username, password=password, email=email, phone=phone, role=role)
	new_user.salt.append(new_salt)
	db.add(new_user)
	db.commit()

async def get_user(user_identificator: Union[int, str]) -> User:
	if type(user_identificator) is str:
		user = db.query(User).filter(User.username == user_identificator).one()
		return user
	else:
		user = db.query(User).filter(User.id == user_identificator).one()
		return user
