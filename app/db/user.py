from typing import Union, List, Dict
from datetime import datetime, time
from app.db.db_setup import db, User, Salt, About, Achievement, Timetable
import hashlib
import bcrypt

class UserAlreadyExists(Exception):
	...

async def create_user(username: str, password_raw: str, email: str, phone: str, role: str) -> None:
	try:
		get_user(username)
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
	

async def get_user(user_identificator: Union[int, str]) -> User:
	if type(user_identificator) is str:
		user = db.query(User).filter(User.username == user_identificator).one()
		return user
	else:
		user = db.query(User).filter(User.id == user_identificator).one()
		return user

async def create_about(user_identificator: Union[int, str],
							name: str, surname: str, city: str, birthday: datetime, gender: str,
							citizenships: List[str], rank: str, salary: int, currency: str, stack: List[str],
							school: str, grade: int, native_language: str, foreign_languages: List[str], can_move: str,
							metro_station: str, github_id: str, vk_id: str, telegram_id: str, 
							timetable: List[Dict], achievements: List[Dict]) -> None:
	user = get_user(user_identificator)
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

async def get_about(user_identificator: Union[int, str]) -> About:
	user = get_user(user_identificator)
	return user.about[0]