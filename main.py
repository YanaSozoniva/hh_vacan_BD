from src.API_hh import HeadHunterAPI
from src.create_db import CreateDB
from src.vacancy import Vacancy
from src.vacancies_list import VacanciesList
from src.db_manager import DBManager


def main():
    """Главная функция приложения"""
    answer_user = input("""Добро пожаловать в программу получения вакансий с сайта hh.ry по 10 топ компаниям с
открытыми вакансиями.
Топ компаний выбирается по заданному Вами ключевому слову (переданное значение ищется в названии и описании
работодателя). Введите запрос (например: IT):\n""")
    vac = HeadHunterAPI()
    employers = vac.get_employers(answer_user)
    create_db = CreateDB()
    create_db.insert_data_employers(employers)

    for id_em in employers:
        hh_vacancies = vac.get_vacancies(id_em['id'])
        vacancies = Vacancy.cast_to_object_list(hh_vacancies)
        vacan_list = VacanciesList(vacancies)
        create_db.insert_data_vacancies(vacan_list)

    db_men = DBManager()

    print("Найденные компании и количество открытых вакансий в каждой компании")
    data_employers = db_men.get_companies_and_vacancies_count()

    for item in data_employers:
        print(f"{item['name_employer']} - {item['count_vacancies']} шт.")

    while True:
        answer_user = input("""Введите название компании, по которой хотите просмотреть вакансии или введите нет:\n""")
        if answer_user.lower() == 'нет':
            break
        else:
            data_vacan = db_men.get_all_vacancies()
            if answer_user.lower() not in [item["employers_name"].lower() for item in data_vacan]:
                print("Компании с таким названием нет. Будьте внимательнее и попробуйте еще раз")
                continue

            data_vacan_filter = [item for item in data_vacan if item["employers_name"].lower() == answer_user.lower()]
            print(f"Вакансии компании {data_vacan_filter[0]["employers_name"]}")
            for item in data_vacan_filter:
                print(f"Вакансия: {item["vacancies_name"]}, зарплата {item["salary_from"]} - {item["salary_to"]} "
                      f"{item["currency"]}. Полная информация по ссылке: {item["url"]}")

    answer_user = input("""Вывести среднюю зарплату вакансий по компаниям? (да/нет):\n""")
    if answer_user.lower() == 'да':
        data_avg = db_men.get_avg_salary()
        for item in data_avg:
            print(f"{item['employers_name']} - {item['avg_salary']}")

    answer_user = input("""Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям?
(да/нет):\n""")
    if answer_user.lower() == 'да':
        data_avg = db_men.get_vacancies_with_higher_salary()
        for item in data_avg:
            print(f"{item['vacancies_name']} - {item['salary_from']} {item['currency']}")

    answer_user = input("""Вывести список всех вакансий, в названии которых содержатся указанное Вами слово?
Если нет - введите 'нет', иначе введите слово:\n""")
    if answer_user.lower() != 'нет':
        data_word = db_men.get_vacancies_with_keyword(answer_user)
        print(f"По вашему запросу найдено {len(data_word)} вакансий")
        for item in data_word:
            print(f"Вакансия: {item["vacancies_name"]}, компании {item["employers_name"]}, "
                  f"зарплата {item["salary_from"]} - {item["salary_to"]} "
                  f"{item["currency"]}. Полная информация по ссылке: {item["url"]}")


if __name__ == '__main__':
    main()
