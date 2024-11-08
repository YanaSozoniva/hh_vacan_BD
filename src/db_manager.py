from src.logger import logger_setup


logger = logger_setup()


class DBManager:
    """Класс для работы с данными в БД"""

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Метод для получения списка всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self) -> list[dict]:
        """Метод получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты
         и ссылки на вакансию."""
        pass

    def get_avg_salary(self) -> list[dict]:
        """Метод получения средней зарплаты по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict]:
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова"""
        pass
