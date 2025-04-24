from src.utils import filter_vacancies


def test_filter_vacancies():
    vacancies = [
        {"title": "Developer", "salary": 60000},
        {"title": "Manager", "salary": None},
        {"title": "Intern", "salary": 40000},
        {"title": "Senior Developer", "salary": 80000},
    ]

    # Тест 1: Фильтрация с минимальной зарплатой 50000
    result = filter_vacancies(vacancies, min_salary=60000)
    expected = [
        {"title": "Developer", "salary": 60000},
        {"title": "Senior Developer", "salary": 80000},
    ]
    assert result == expected