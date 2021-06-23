from typing import List
from app.db.db_setup import db, Tech, Language

async def get_techs() -> List[str]:
	raw_techs = db.query(Tech).all()
	techs = []
	for tech in raw_techs:
		techs.append(tech.title)
	return techs

async def get_languages() -> List[str]:
	raw_languages = db.query(Language).all()
	languages = []
	for language in raw_languages:
		languages.append(language.title)
	return languages


