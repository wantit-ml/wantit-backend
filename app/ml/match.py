from typing import List
from app.db.db_setup import About, Vacancy

""" 
should be called as 
 users_for_vacancy = await MatchForHR.search_users(vacancy, list_of_about_objects)
"""


class MatchForHR():
    @classmethod
    async def search_users(cls, vacancy: Vacancy, users_list: List[About]) -> List[int]:
        matched_users_ids = []
        for candidate in users_list:
            if vacancy.code & candidate.code >= vacancy.code:
                matched_users_ids.append(candidate.id)
        return matched_users_ids


""" 
should be called as 
 users_for_vacancy = await MatchForUser.search_users(about_object, list_of_vacancy_objects)
"""


class MatchForUser():
    @classmethod
    async def search_vacancies(cls, user_info: About, vacances_list: List[Vacancy]) -> List[int]:
        matched_vacances_ids = []
        for sample_vacancy in vacances_list:
            if sample_vacancy.code & user_info.code >= sample_vacancy.code:
                matched_vacances_ids.append(sample_vacancy.id)
        return matched_vacances_ids
