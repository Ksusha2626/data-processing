from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient

"""
Написать приложение, которое собирает основные новости с сайта на выбор 
news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. 
Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
Сложить собранные новости в БД
"""

MAIL_URL = 'https://news.mail.ru/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/97.0.4692.71 Safari/537.36'}


def db_upload(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    mail_ru = db.mail_ru
    mail_ru.create_index('link', name='index', unique=True)

    if mail_ru.count_documents({}) == 0:
        mail_ru.insert_many(data)
    else:
        for news in data:
            mail_ru.replace_one({'link': news['link']}, news, upsert=True)
    for news in mail_ru.find({}):
        pprint(news)
    # mail_ru.drop()
    # client.drop_database('news')


def mail_ru_news_parser():
    dom = html.fromstring(requests.get(MAIL_URL, headers=HEADERS).text)
    news_links = dom.xpath('//a[contains(@class, "topnews__item")]/@href')

    news = []
    for url in news_links:
        dom = html.fromstring(requests.get(url, headers=HEADERS).text)

        source = dom.xpath('.//a[contains(@class, "breadcrumbs__link")]/@href')[0]
        title = dom.xpath('.//h1/text()')[0]
        datetime = dom.xpath('.//span[contains(@class, "js-ago")]/@datetime')[0]

        news.append({
            'link': url,
            'source': source,
            'title': title,
            'datetime': datetime,
        })
    db_upload(news)
    return news


if __name__ == '__main__':
    mail_ru_news_parser()
