import psycopg2

from src.config import config
from src.logger import logger_setup

logger = logger_setup()


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str = "headhunter"):
        self.db_name = database_name
        self.__params = config()
        self.conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Метод для получения списка всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            self.cur.execute(
                """SELECT employers.name, COUNT(vacancies.id_employer) as count_vacancies FROM employers
             LEFT JOIN vacancies USING (id_employer) GROUP BY employers.name"""
            )

            data = self.cur.fetchall()
            data_dict = [{"name_employer": d[0], "count_vacancies": d[1]} for d in data]
            return data_dict

    def get_all_vacancies(self) -> list[dict]:
        """Метод получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию."""
        with self.conn:
            self.cur.execute(
                """SELECT vacancies.name, employers.name, salary_from, salary_to, currency, url
             FROM vacancies
             LEFT JOIN employers USING (id_employer)"""
            )

            data = self.cur.fetchall()
            data_dict = [
                {
                    "vacancies_name": d[0],
                    "employers_name": d[1],
                    "salary_from": d[2],
                    "salary_to": d[3],
                    "currency": d[4],
                    "url": d[5],
                }
                for d in data
            ]
            return data_dict

    def get_avg_salary(self) -> list[dict]:
        """Метод получения средней зарплаты по вакансиям."""
        with self.conn:
            self.cur.execute(
                """SELECT  employers.name, ROUND (avg(salary_from), 2) FROM vacancies
             LEFT JOIN employers USING (id_employer)
            Group by employers.name"""
            )

            data = self.cur.fetchall()
            data_dict = [{"employers_name": d[0], "avg_salary": d[1]} for d in data]
            return data_dict

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn:
            self.cur.execute(
                """SELECT  vacancies.name, salary_from, currency FROM vacancies
             WHERE salary_from > (SELECT avg(salary_from) FROM vacancies)"""
            )

            data = self.cur.fetchall()
            data_dict = [{"vacancies_name": d[0], "salary_from": d[1], "currency": d[2]} for d in data]
            return data_dict

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict]:
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn:
            self.cur.execute(
                f"SELECT  vacancies.name, employers.name, salary_from, salary_to, currency, url"
                f" FROM vacancies"
                f" LEFT JOIN employers USING (id_employer)"
                f" WHERE vacancies.name LIKE '%{keyword}%'"
            )

            data = self.cur.fetchall()
            data_dict = [
                {
                    "vacancies_name": d[0],
                    "employers_name": d[1],
                    "salary_from": d[2],
                    "salary_to": d[3],
                    "currency": d[4],
                    "url": d[5],
                }
                for d in data
            ]
            return data_dict
