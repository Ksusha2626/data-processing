from pprint import pprint

import lxml.html
import requests
from lxml import html

MAIL_URL = 'https://news.mail.ru/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/97.0.4692.71 Safari/537.36'}


response = requests.get(MAIL_URL, headers=HEADERS)

dom = html.fromstring(response.text)

titles = dom.xpath()