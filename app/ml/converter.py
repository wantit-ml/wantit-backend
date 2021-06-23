from typing import Union, List
from app.db.db_setup import About, Vacancy

""" 
converts About or Vacancy class to code num
 
 after declaring 
 converter = Converter(techs_list, languages_list) 
 that should be done once
 
 than for every new or changed application/vacancy you should call 
 converter.convert(object_to_code)
 and add the result of function to "code" field in DB
"""

class Converter():
    def __init__(self, baseline_techs: List[str], baseline_lanuages: List[str]):
        self.baseline_techs = baseline_techs
        self.baseline_languages = baseline_lanuages

    async def convert(self, data: Union[About, Vacancy]) -> int:
        stack_code = ['0' for i in range(len(self.baseline_techs))]
        for tech_name in data.stack:
            stack_code[self.baseline_techs.index(tech_name)] = '1'

        lang_code = ['0' for i in range(len(self.baseline_languages))]
        for lang_name in data.foreign_languages:
            lang_code[self.baseline_languages.index(lang_name)] = '1'

        return int(''.join(stack_code + lang_code), 2)
