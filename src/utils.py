from typing import List


def filter_vacancies(vacancies: List[dict], min_salary: float = 0) -> List[dict]:
    """Фильтр вакансий по зарплате"""
    return [
        vacancy
        for vacancy in vacancies
        if vacancy["salary"] and vacancy["salary"] >= min_salary]
