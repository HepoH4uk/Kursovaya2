import json
from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractFileHandler(ABC):
    """Абстрактный класс обработки файла"""
    def __init__(self, filename):
        self.__filename = filename

    @abstractmethod
    def add_vacancy(self, vacancy) -> List[Dict]:
        """Добавить вакансию в файл"""
        pass

    @abstractmethod
    def save_data(self, data: List[Dict]):
        """Сохранение данных"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """Получить вакансии из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, title):
        """Удалить вакансию по названию."""
        pass


class JSONFileHandler(AbstractFileHandler):
    """Класс обработки файла"""
    def __init__(self, filename = "vacancies.json"):
        super().__init__(filename)

    def add_vacancy(self, vacancy) -> List[Dict]:
        """Добавляем вакансию в JSON-файл"""
        vacancies = self.get_vacancies()
        try:
            if vacancy not in vacancies:
                vacancies.append(vacancy)
                with open(self._AbstractFileHandler__filename, 'w') as file:
                    json.dump(vacancies, file, indent=4)
        except FileNotFoundError:
            return []

        # try:
        #     with open(self.__filename, "r", encoding="utf-8") as file:
        #         return json.load(file)
        # except FileNotFoundError:
        #     return []

    def save_data(self, data):
        """Сохраняем вакансию в файл"""
        try:
            with open("vacancies.json", "r", encoding="utf-8") as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):  # Проверяем, что это список
                    existing_data = (
                        []
                    )  # Если это не список, инициализируем пустой список
        except FileNotFoundError:
            existing_data = []  # Если файл не найден, создаем новый список

        existing_data.extend(data)  # Теперь это безопасно

        with open("vacancies.json", "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria):
        """Получить вакансии из файла по указанным критериям."""
        filtered_vacancies = []
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():  # Проверяем, что строка не пустая
                        data = json.loads(line)
                        if criteria.lower() in data.get("name", "").lower():
                            filtered_vacancies.append(data)
        except FileNotFoundError:
            print(f"Файл {self.__filename} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

        return filtered_vacancies  # Возвращаем отфильтрованные вакансии

    def delete_vacancy(self, vacancy_name):
        """Удалить вакансии из файла."""
        data = self.add_vacancy()
        # Удаляем вакансию из списка
        data = [vacancy for vacancy in data if vacancy.get("name") != vacancy_name]
        self.save_data(data)
