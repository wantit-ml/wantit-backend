from typing import Union, List, Dict
from datetime import datetime
from app.db.db_setup import db, User, Salt, About, Achievement, Timetable, Session
import hashlib
import bcrypt
import uuid

class UserAlreadyExists(Exception):
	...

async def create_user(username: str, password_raw: str, email: str, phone: str, role: str) -> None:
	try:
		await get_user(username)
	except:
		salt = bcrypt.gensalt()
		hash_object = hashlib.sha256(password_raw.encode() + salt)
		password = hash_object.hexdigest()
		new_salt = Salt(salt=salt)
		new_user = User(username=username, password=password, email=email, phone=phone, role=role)
		new_user.salt.append(new_salt)
		db.add(new_user)
		db.commit()
	else:
		raise UserAlreadyExists
	

async def get_user(user_identifier: Union[int, str]) -> User:
	if type(user_identifier) is str:
		user = db.query(User).filter(User.username == user_identifier).one()
		return user
	else:
		user = db.query(User).filter(User.id == user_identifier).one()
		return user

async def create_about(user_identifier: Union[int, str],
							name: str, surname: str, city: str, birthday: datetime, gender: str,
							citizenships: List[str], rank: str, salary: int, currency: str, stack: List[str],
							school: str, grade: int, native_language: str, foreign_languages: List[str], can_move: str,
							metro_station: str, github_id: str, vk_id: str, telegram_id: str, 
							timetable: List[Dict], achievements: List[Dict]) -> None:
	user = await get_user(user_identifier)
	new_about = About(name=name, surname=surname, city=city, birthday=birthday, gender=gender, citizenships=citizenships, rank=rank, 
		salary=salary, currency=currency, stack=stack, school=school, grade=grade, native_language=native_language,
		foreign_languages=foreign_languages, can_move=can_move, metro_station=metro_station, github_id=github_id, vk_id=vk_id,
		telegram_id=telegram_id)
	for item in timetable:
		new_time_record = Timetable(day=item["day"], time=item["time"])
		new_about.timetable.append(new_time_record)
	for achievement in achievements:
		new_achievement = Achievement(type=achievement["type"], title=achievement["title"],
			level=achievement["level"], role=achievement["role"], file=achievement["file"],
			description=achievement["description"])
		new_about.achievements.append(new_achievement)
	user.about.append(new_about)
	db.commit()

async def get_about(user_identifier: Union[int, str]) -> About:
	user = await get_user(user_identifier)
	return user.about[0]

async def create_session(user_identifier: Union[int, str]) -> str:
	session_id = uuid.uuid1()
	new_session = Session(session_id=session_id)
	user = await get_user(user_identifier)
	user.sessions.append(new_session)
	db.commit()
	return session_id

async def expire_session(session_id: str) -> None:
	db.query(Session).filter(Session.session_id ==
                          session_id).delete(synchronize_session="fetch")
	db.commit()

async def verify_session(user_identifier: Union[int, str], session_id: str) -> bool:
	user = await get_user(user_identifier)
	is_valid = False
	for session in user.sessions:
		if session.session_id == session_id:
			is_valid = True
			break
	return is_valid

async def verify_role(user_identifier: Union[int, str], role) -> bool:
	user = await get_user(user_identifier)
	return user.role == role
