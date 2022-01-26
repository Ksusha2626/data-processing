import json
from pprint import pprint
import pandas as pd

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
PAGE = 0
params = {'area': MINSK_AREA,
          'text': VACANCY,
          'page': PAGE}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/97.0.4692.71 Safari/537.36'}

dom = BeautifulSoup(requests.get(HH_URL, params=params, headers=headers).text,
                    'html.parser')

job_list = dom.select('div.vacancy-serp-item')

jobs = []
while job_list:
    for job in job_list:
        title_info = job.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        job_data = {'title': title_info.getText().replace('\xa0', ' '),
                    'link': title_info.get('href')}
        salary = job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary_data = {'min': int(), 'max': int(), 'currency': ''}
        if salary:
            salary_list = salary.getText().replace('\u202f', '').split()
            if salary_list[0].isalpha():
                if salary_list[0] == 'от':
                    salary_data['min'] = int(salary_list[1])
                    salary_data['max'] = None
                    salary_data['currency'] = salary_list[-1]
                else:
                    salary_data['min'] = None
                    salary_data['max'] = int(salary_list[1])
                    salary_data['currency'] = salary_list[-1]
            else:
                salary_data['min'] = int(salary_list[0])
                salary_data['max'] = int(salary_list[2])
                salary_data['currency'] = salary_list[-1]
        else:
            salary_data['min'] = None
            salary_data['max'] = None
            salary_data['currency'] = None

        job_data['source'] = 'https://hh.ru'
        job_data['salary'] = salary_data

        jobs.append(job_data)
    PAGE += 1
    params.update({'page': PAGE})
    dom = BeautifulSoup(
        requests.get(HH_URL, params=params, headers=headers).text,
        'html.parser')
    job_list = dom.select('div.vacancy-serp-item')

df = pd.DataFrame(jobs)
df.to_csv('output.csv', sep='\t', encoding='utf-8')
print(df)
pprint(jobs)

with open("jobs_info.json", 'w') as f:
    f.write(
        json.dumps(jobs, indent=4, ensure_ascii=False))

# 2 salary-parsing algorithm option
# salary_data = {'min': None, 'max': None, 'currency': ''}
#     if salary:
#         salary_list = salary.getText().replace('\u202f', '').split()
#         salary = []
#         for x in salary_list:
#             try:
#                 salary.append(int(x))
#             except ValueError:
#                 salary.append(x)
#         for i, el in enumerate(salary):
#             next_el = salary[i + 1] if len(salary) - 1 != i else salary[i]
#             if isinstance(el, str):
#                 if el == 'от':
#                     salary_data['min'] = next_el
#                 elif el == 'до':
#                     salary_data['max'] = next_el
#                 elif el == '–':
#                     salary_data['min'] = salary[i - 1]
#                     salary_data['max'] = next_el
#                 else:
#                     salary_data['currency'] += el
#             continue
