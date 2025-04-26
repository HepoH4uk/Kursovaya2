from unittest.mock import Mock, patch
from src.api import HeadHunterAPI
from src.vacancies import Vacancy
import pytest

def test_connect_success():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        response = api.connect()
        assert response.status_code == 200, "Ошибка: Метод connect не вернул статус 200"
        mock_get.assert_called_once_with(api._HeadHunterAPI__base_url)


def test_connect_failure():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        try:
            api.connect()
        except Exception as e:
            assert str(e) == "Ошибка подключения: 404"


def test_get_vacancies_success():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": 1, "name": "Vacancy 1"}, {"id": 2, "name": "Vacancy 2"}]}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("developer")

        assert len(vacancies) == 2, "Ошибка: Должно быть 2 вакансии"
        assert vacancies[0]["name"] == "Vacancy 1"
        mock_get.assert_called_with(
            api._HeadHunterAPI__base_url, params={"text": "developer", "per_page": 20})


def test_vacancy_init():
    vacancy = Vacancy("1", "Test Vacancy", 1000.0, "http://example.com")
    assert vacancy.id == "1"
    assert vacancy.title == "Test Vacancy"
    assert vacancy.salary == 1000.0
    assert vacancy.url == "http://example.com"


def test_vacancy_salary_setter():
    vacancy = Vacancy("1", "Test Vacancy", 1000.0, "http://example.com")
    vacancy.salary = 2000.0
    assert vacancy.salary == 2000.0


def test_vacancy_wrong_salary():
    vacancy = Vacancy("1", "Test Vacancy", 1000.0, "http://example.com")
    with pytest.raises(ValueError) as er:
        vacancy.salary = -2000.0
    assert str(er.value) == "Заработная плата не может быть отрицательной"


def test_vacancy_wrong_id():
    vacancy = Vacancy("1", "Test Vacancy", 1000.0, "http://example.com")
    with pytest.raises(ValueError) as er:
        vacancy.id = None
    assert str(er.value) == "ID должен быть непустой строкой"


def test_vacancy_wrong_title():
    vacancy = Vacancy("1", "Test Vacancy", 1000.0, "http://example.com")
    with pytest.raises(ValueError) as er:
        vacancy.title = None
    assert str(er.value) == "Название должно быть непустой строкой"
