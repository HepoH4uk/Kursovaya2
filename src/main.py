from src.api import HeadHunterAPI
from src.utils import filter_vacancies
from src.vacancies import Vacancy
from src.handler import JSONFileHandler


def main():
    api = HeadHunterAPI()
    file_manager = JSONFileHandler('vacancies.json')  # Убедитесь, что вы передаете имя файла

    while True:
        print("""1. Получить вакансии по запросу
2. Получить минимальную зарплату по вакансии
3. Удалить вакансию по названию
4. Выход""")
        choice = input("\nВыберите действие: ")

        if choice == '1':
            keyword = input('\nВведите ключевое слово для поиска вакансий: ')
            vacancies_data = api.get_vacancies(keyword)
            vacancies = []
            for item in vacancies_data:
                vacancy = Vacancy(
                    id=item['id'],
                    title=item['name'],
                    salary=item['salary']['from'] if item['salary'] else 0,
                    url=item['alternate_url']
                )
                vacancies.append(vacancy)

            file_manager.save_data([{
                'id': vacancy.id,
                'title': vacancy.title,
                'salary': vacancy.salary,
                'url': vacancy.url
            } for vacancy in vacancies])
            print(f"\nДобавлена вакансия: {vacancy.title}")

        elif choice == '2':
            try:
                min_salary = float(input('\nВведите минимальную зарплату: '))
                filtered_vacancies = filter_vacancies([{
                    'id': vacancy.id,
                    'title': vacancy.title,
                    'salary': vacancy.salary,
                    'url': vacancy.url
                } for vacancy in vacancies], min_salary)
                print('\nОтфильтрованные вакансии: ')
                for vacancy in filtered_vacancies:
                    print(vacancy)
            except UnboundLocalError as e:
                print(f"\nПроизошла ошибка: {e}\nДля начала выберите вакансию которая вас интересует")

        elif choice == '3':
            title = input("\nВведите название вакансии для удаления: ")
            file_manager.delete_vacancy(title)
            print(f"\nВакансия '{title}' удалена.")

        elif choice == '4':
            break

        else:
            print("\nНеверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
