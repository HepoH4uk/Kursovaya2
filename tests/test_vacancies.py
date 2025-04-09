from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


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
