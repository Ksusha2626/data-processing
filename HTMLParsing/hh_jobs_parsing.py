import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

"""
Необходимо собрать информацию о вакансиях на вводимую должность.
Приложение должно анализировать несколько страниц сайта.
Поля:
1. Наименование вакансии.
2. Предлагаемую зарплату (разносим в три поля: мин и макс и валюта.
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия
"""

HH_URL = 'https://hh.ru/search/vacancy'
MINSK_AREA = 1002
VACANCY = 'QA'
PAGE = 2
params = {'area': MINSK_AREA,
          'text': VACANCY,
          'page': PAGE}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/97.0.4692.71 Safari/537.36'}

response = requests.get(HH_URL, params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.select('div.vacancy-serp-item')

vacancies_list = []
for vacancy in vacancies:
    vacancies_data = {}
    title_info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    title = title_info.getText().replace('\xa0', ' ')
    vacancy_url = title_info.get('href')
    salary = vacancy.find('span',
                          {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary_data = {'min': None, 'max': None, 'currency': ''}
    if salary:
        salary_list = salary.getText().replace('-->', '').replace('<!--', '').replace('\u202f', '').split()
        salary = []
        for x in salary_list:
            try:
                salary.append(int(x))
            except ValueError:
                salary.append(x)
        for i, el in enumerate(salary):
            next_el = salary[i + 1] if len(salary) - 1 != i else salary[i]
            if isinstance(el, str):
                if el == 'от':
                    salary_data['min'] = next_el
                    i += 1
                    continue
                if el == 'до':
                    salary_data['max'] = next_el
                    i += 1
                    continue
                if el == '–':
                    salary_data['min'] = salary[i - 1]
                    salary_data['max'] = next_el
                    continue
                else:
                    salary_data['currency'] += el
            continue
    vacancies_data['title'] = title
    vacancies_data['salary'] = salary_data
    vacancies_data['vacancy_url'] = vacancy_url
    vacancies_data['source'] = 'https://hh.ru'

    vacancies_list.append(vacancies_data)

pprint(vacancies_list)

with open("jobs_info.json", 'w') as f:
    f.write(
        json.dumps(vacancies_list, indent=4, ensure_ascii=False))
