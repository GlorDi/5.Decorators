import os
import datetime
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def logger(old_function):

    def new_function(*args, **kwargs):

        value = old_function(*args, **kwargs)

        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'Функция {old_function.__name__} была вызвана в {datetime.datetime.now()} с аргументами {args=} и {kwargs=}\nВозвращаемое значение: {value}\n\n')
        return value

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            value = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(
                    f'Функция {old_function.__name__} была вызвана в {datetime.datetime.now()} с аргументами {args=} и {kwargs=}\nВозвращаемое значение: {value}\n\n')
                return value
        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()


def logger(old_function):
    def new_function(*args, **kwargs):
        value = old_function(*args, **kwargs)

        with open('parser.log', 'a', encoding='utf-8') as f:
            f.write(
                f'Функция {old_function.__name__} была вызвана в {datetime.datetime.now()} с аргументами {args=} и {kwargs=}\nВозвращаемое значение: {value}\n\n')
        return value

    return new_function


@logger
def parser():
    def get_headers():
        return Headers(browser='chrome', os='win').generate()

    HOST = 'https://hh.ru/search/vacancy?text=python&area=1&area=2'
    html = requests.get(HOST, headers=get_headers()).text

    soup = BeautifulSoup(html, features='lxml')
    all_vacancies = soup.find(id='a11y-main-content')
    vacancy = all_vacancies.find_all(class_='serp-item')

    description_list = []
    for item in vacancy:
        description_vacancy = item.find(class_='vacancy-serp-item__layout')
        description = description_vacancy.find(class_='g-user-content').text
        if 'Django' in description and 'Flask' in description:
            description_list.append(item)

    vacancy_list = []
    for word in description_list:
        title = word.find('a', class_='serp-item__title').text
        link_tag = word.find('a', class_='serp-item__title')
        link = link_tag['href']
        try:
            salary_tag = word.find('span', class_='bloko-header-section-3')
            salary = salary_tag.text
        except Exception:
            salary = 'Не указана'
        company_tag = word.find('a', class_='bloko-link bloko-link_kind-tertiary')
        company = company_tag.text
        city_tag = word.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
        city = city_tag.text

        vacancy_list.append({

            'Название': title,
            'Зарплата': salary,
            'Компания': company,
            'Город': city,
            'Ссылка': link

        })

    return vacancy_list


if __name__ == '__main__':
    parser()