from src.API_hh import HeadHunterAPI
from src.create_db import CreateDB
from src.vacancy import Vacancy
from src.vacancies_list import VacanciesList


def main():
    vac = HeadHunterAPI()
    employers = vac.get_employers("it")
    db = CreateDB()
    db.insert_data_employers(employers)

    for id_em in employers:
        hh_vacancies = vac.get_vacancies(id_em['id'])
        vacancies = Vacancy.cast_to_object_list(hh_vacancies)
        vacn_list = VacanciesList(vacancies)
        db.insert_data_vacancies(vacn_list)


if __name__ == '__main__':
    main()
