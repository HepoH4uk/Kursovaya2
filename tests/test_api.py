from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


def test_connect_failure():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        try:
            api.connect()
            assert False, "Ожидалось исключение при статусе 404"
        except Exception as e:
            assert str(e) == "Ошибка подключения: 404"


def test_get_vacancies_no_items():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [],
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("разработчик")
        assert len(vacancies) == 0, "Ошибка: Должно быть 0 вакансий"
        mock_get.assert_called()
