from os import SEEK_CUR
from typing import Union, List, Dict, Optional
from datetime import datetime
from app.db.db_setup import (
    Vacancy,
    db,
    User,
    Salt,
    About,
    Achievement,
    Timetable,
    Session,
    Tech,
    Language,
)
from app.db.tags import get_techs, get_languages
from app.ml.converter import Converter
from app.ml.match import MatchForHR
from app.db.error_boundary import error_boundary
import hashlib
import bcrypt
import uuid


class UserAlreadyExists(Exception):
    ...


class WrongPassword(Exception):
    ...


@error_boundary
async def create_user(
    username: str, password_raw: str, email: str, phone: str, role: str
) -> None:
    try:
        await get_user(username)
    except:
        salt = bcrypt.gensalt()
        hash_object = hashlib.sha256(
            password_raw.encode() + salt)
        password = hash_object.hexdigest()
        new_salt = Salt(salt=salt.decode())
        new_user = User(
            username=username, password=password, email=email, phone=phone, role=role
        )
        new_user.salt.append(new_salt)
        db.add(new_user)
        db.commit()
    else:
        raise UserAlreadyExists("UserAlreadyExists")


async def get_user(user_identifier: Union[int, str]) -> User:
    user_identifier = int(user_identifier) if type(
        user_identifier) == str and user_identifier.isdigit() else user_identifier
    if type(user_identifier) is str:
        user = db.query(User).filter(User.username == user_identifier).one()
        return user
    else:
        user = db.query(User).filter(User.id == user_identifier).one()
        return user


@error_boundary
async def create_about(
    user_identifier: Union[int, str],
    name: str,
    surname: str,
    description: str,
    city: str,
    birthday: datetime,
    gender: str,
    citizenships: List[str],
    rank: str,
    salary: int,
    currency: str,
    stack: List[str],
    school: str,
    age: int,
    native_language: str,
    foreign_languages: List[str],
    can_move: str,
    metro_station: str,
    github_id: str,
    vk_id: str,
    telegram_id: str,
    timetable: List[Dict],
    achievements: List[Dict],
) -> None:
    user = await get_user(user_identifier)
    new_about = About(
        name=name,
        surname=surname,
        description=description,
        city=city,
        birthday=birthday,
        gender=gender,
        citizenships=citizenships,
        rank=rank,
        salary=salary,
        currency=currency,
        stack=stack,
        school=school,
        age=age,
        native_language=native_language,
        foreign_languages=foreign_languages,
        can_move=can_move,
        metro_station=metro_station,
        github_id=github_id,
        vk_id=vk_id,
        telegram_id=telegram_id,
    )
    for item in timetable:
        new_time_record = Timetable(day=item["day"], time=item["time"])
        new_about.timetable.append(new_time_record)
    for achievement in achievements:
        new_achievement = Achievement(
            type=achievement["type"],
            title=achievement["title"],
            level=achievement["level"],
            role=achievement["role"],
            file=achievement["file"],
            description=achievement["description"],
        )
        new_about.achievements.append(new_achievement)
    user.about.append(new_about)
    db.commit()
    for tech in stack:
        try:
            new_tech = Tech(title=tech.lower().strip().title())
            db.add(new_tech)
            db.commit()
        except:
            db.rollback()
            continue
    for language in foreign_languages:
        try:
            new_language = Language(title=language.lower().strip().title())
            db.add(new_language)
            db.commit()
        except:
            db.rollback()
            continue
    db.commit()
    await convert_about(user_identifier)


async def get_about(user_identifier: Union[int, str]) -> About:
    user = await get_user(user_identifier)
    return user.about[0]


@error_boundary
async def create_session(user_identifier: Union[int, str], password_raw: str) -> str:
    user = await get_user(user_identifier)
    salt = user.salt[0].salt
    hash_object = hashlib.sha256((password_raw + salt).encode())
    password = hash_object.hexdigest()
    if not user.password == password:
        raise WrongPassword("Bad password")
    session_id = str(uuid.uuid1())
    new_session = Session(session_id=session_id)
    user.sessions.append(new_session)
    db.commit()
    return session_id


@error_boundary
async def expire_session(session_id: str) -> None:
    db.query(Session).filter(Session.session_id == session_id).delete(
        synchronize_session="fetch"
    )
    db.commit()


async def verify_session(user_identifier: Union[int, str], session_id: str) -> User:
    user = await get_user(user_identifier)
    is_valid = session_id in [session.session_id for session in user.sessions]
    if not is_valid:
        return None
    return user


async def verify_role(user_identifier: Union[int, str], role) -> bool:
    user = await get_user(user_identifier)
    return user.role == role


@error_boundary
async def convert_about(user_identifier: Union[int, str]) -> None:
    about = await get_about(user_identifier)
    techs = await get_techs()
    languages = await get_languages()
    converter = Converter(techs, languages)
    code = await converter.convert(about)
    about.code = code
    db.commit()


async def get_matching_users(vacancy_id: int) -> List[User]:
    from app.db.vacancy import get_vacancy_by_id
    users = db.query(User).all()
    users_list = []
    for user in users:
        try:
            users_list.append(user.about[0])
        except:
            continue
    vacancy = await get_vacancy_by_id(vacancy_id)
    matching_users_ids = await MatchForHR.search_users(vacancy, users_list)
    matching_users = []
    for user in users:
        if user.id in matching_users_ids:
            matching_users.append(user)
    print(matching_users)
    return matching_users


async def get_role_by_session_id(session_id: str) -> str:
    session = db.Query(Session).filter(Session.session_id == session_id).one()
    user = await get_user(session.user_id)
    return user.role

async def get_all_abouts() -> List[About]:
    abouts_list = db.Query(About).all()
    return abouts_list
