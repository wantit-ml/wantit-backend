from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	email = Column(String)
	phone = Column(String)
	role = Column(String)
	about = relationship("About", backref="users")
	salt = relationship("Salt", backref="users")
	sessions = relationship("Session", backref="users")

class Session(Base):
	__tablename__ = "session"
	id = Column(Integer, primary_key=True)
	session_id = Column(String)
	user_id = Column(Integer, ForeignKey("users.id"))

class About(Base):
	__tablename__ = "about"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	name = Column(String)
	surname = Column(String)
	city = Column(String)
	birthday = Column(DateTime)
	gender = Column(String)
	citizenships = Column(ARRAY(String))
	rank = Column(String)
	salary = Column(Integer)
	currency = Column(String)
	stack = Column(ARRAY(String))
	school = Column(String)
	age = Column(Integer)
	native_language = Column(String)
	foreign_languages = Column(ARRAY(String))
	can_move = Column(String)
	timetable = relationship("Timetable", backref="about")
	metro_station = Column(String)
	github_id = Column(String)
	vk_id = Column(String)
	telegram_id = Column(String)
	code = Column(Integer)
	achievements = relationship("Achievement", backref="about")

class Timetable(Base):
	__tablename__ = "timetable"
	id = Column(Integer, primary_key=True)
	day = Column(String)
	time = Column(String) # e.g. times = ["18:00-19:00", "12:00-13:00" etc]
	about_id = Column(Integer, ForeignKey("about.id"))

class Achievement(Base):
	__tablename__ = "achievements"
	id = Column(Integer, primary_key=True)
	type = Column(String)
	title = Column(String)
	level = Column(String)
	role = Column(String)
	file = Column(String)
	description = Column(String)
	about_id = Column(Integer, ForeignKey("about.id"))

class Salt(Base):
	__tablename__ = "salt"
	id = Column(Integer, primary_key=True)
	salt = Column(String)
	user_id = Column(Integer, ForeignKey("users.id"))

class Vacancy(Base):
	__tablename__ = "vacancy"
	id = Column(Integer, primary_key=True)
	title = Column(String)
	vacation_code = Column(String)
	description = Column(String)
	stack = Column(ARRAY(String))
	salary = Column(Integer)
	currency = Column(String)
	city = Column(String)
	address = Column(String)
	type_of_vacancy = Column(String)
	author = Column(String)
	phone = Column(String)
	email = Column(String)
	code = Column(Integer)

class Tech(Base):
	__tablename__ = "techs"
	id = Column(Integer, primary_key=True)
	title = Column(String, unique=True)

class Language(Base):
	__tablename__ = "languages"
	id = Column(Integer, primary_key=True, unique=True)
	title = Column(String)

engine = create_engine(os.environ["PSQL_LINK"])
Base.metadata.bind = engine
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
db = DBSession()
