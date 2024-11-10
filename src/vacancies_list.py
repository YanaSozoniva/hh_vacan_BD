from typing import Any


class VacanciesList:
    """Класс для работы со списком вакансий"""

    __slots__ = ("__vacancies", "index")

    def __init__(self, vacancies: list[Any] = None) -> None:
        """Конструктор для инициализации экземпляра класса."""
        if vacancies is None:
            self.__vacancies = []
        else:
            self.__vacancies = vacancies
        self.index = 0

    @property
    def vacancies(self):
        """Геттер для корректного вывода списка вакансий"""
        vacancy_str = ""
        for vacancy in self.__vacancies:
            vacancy_str += f"{str(vacancy)}\n"
        return vacancy_str

    def __len__(self):
        """Метод для подсчета количества вакансий в списке"""
        return len(self.__vacancies)

    def __iter__(self):
        """Возвращает итератор."""
        self.index = 0
        return self

    def __next__(self):
        """Возвращает следующую вакансию из списка вакансий"""
        if self.index < len(self.__vacancies):
            vacancy = self.__vacancies[self.index]
            self.index += 1
            return vacancy
        else:
            raise StopIteration

    def __getitem__(self, item):
        """Возвращает вакансию из списка по указанному индексу"""
        return self.__vacancies[item]
