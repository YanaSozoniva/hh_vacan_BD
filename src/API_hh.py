from typing import Any

import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    __url: str
    __params: dict
    __vacancies: list
    __employers: list

    def __init__(self) -> None:
        """Инициализация экземпляров класса HeadHunterAPI"""

        self.__vacancies = []
        self.__employers = []

    def __is_connect(self, url: str) -> bool:
        """Метод для подключения к API"""
        self.__url = url
        response = requests.get(self.__url)
        if response.status_code == 200:
            return True
        raise ValueError("Не удалось получить информацию")

    def get_employers(self, keyword: str) -> list[dict[Any, Any]]:
        """Метод получения информации по работодателям по ключевому слову, переданное значение ищется в названии
         и описании работодателя"""
        if self.__is_connect('https://api.hh.ru/employers'):
            self.__params = {'text': keyword, 'only_with_vacancies': True, 'sort_by': 'by_vacancies_open', 'page': 0,
                             'per_page': 10}
            response = requests.get(self.__url, params=self.__params)
            print(response.json()["per_page"])
            employers = response.json()["items"]
            self.__employers.extend(employers)

        return self.__employers

    def get_vacancies(self, employer: str) -> list[dict[Any, Any]]:
        """Метод получения вакансия с сайта hh.ry по указанному id работодателя"""
        self.__params = {"host": "hh.ru", "employer_id": employer}
        if self.__is_connect('https://api.hh.ru/vacancies'):
            response = requests.get(self.__url, params=self.__params)
            if len(response.json()["items"]) <= 0:
                raise ValueError("По указанному запросу нет вакансий")
            else:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
        return self.__vacancies


if __name__ == "__main__":
    vac = HeadHunterAPI()
    print(vac.get_employers('it'))
    print(vac.get_vacancies('78638'))
