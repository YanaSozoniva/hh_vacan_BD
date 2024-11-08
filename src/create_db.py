from src.logger import logger_setup
from src.config import config

import psycopg2

logger = logger_setup()


class CreateDB:
    """Класс для создания базы данных и заполнения"""

    def __init__(self, database_name: str = "headhunter"):
        self.db_name = database_name
        self.__params = config()

        self.__create_db()
        self._create_tables()

    def __create_db(self) -> None:
        """Метод создания БД"""

        logger.info('Подключение к базе данных postgres')

        conn = psycopg2.connect(dbname='postgres', **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        logger.info('Удаление базы данных, если она существует')

        cur.execute(f"DROP DATABASE  IF EXISTS {self.db_name}")
        logger.info('Создание новой')
        cur.execute(f"CREATE DATABASE {self.db_name}")

        conn.close()

    def _create_tables(self) -> None:
        """Метод создания таблиц Работодатель и вакансии"""
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        logger.info("Создание таблицы Работодатель")
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                id_employer INT PRIMARY KEY,
                name VARCHAR(255)
                )
                """)

        with conn.cursor() as cur:
            logger.info("Создание таблицы Вакансии")

            cur.execute("""
                    CREATE TABLE vacancies (
                        id_vacancy SERIAL PRIMARY KEY,
                        id_employer INT REFERENCES employers(id_employer),
                        name VARCHAR(255) NOT NULL, 
                        salary_from INT, 
                        salary_to INT, 
                        currency VARCHAR(5),
                        url VARCHAR(255), 
                        requirements TEXT

                    )
                """)

        conn.commit()
        conn.close()
        logger.info("БД и таблицы в ней успешно созданы")


if __name__ == "__main__":
    db = CreateDB()
