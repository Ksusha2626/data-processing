from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from Selenium.locators import MvideoLocators
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

M_VIDEO_URL = 'https://www.mvideo.ru/'
options = Options()
options.add_argument("start-maximized")
# options.add_argument("--headless")


def db_upload(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client['shop']
    mvideo_trends = db.mvideo_trends
    mvideo_trends.create_index('link', name='index', unique=True)

    if mvideo_trends.count_documents({}) == 0:
        mvideo_trends.insert_many(data)
    else:
        for item in data:
            mvideo_trends.replace_one({'link': item['link']}, item, upsert=True)
    for item in mvideo_trends.find({}):
        pprint(item)
    # mvideo_trends.drop()
    # client.drop_database('shop')


def m_video():
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(M_VIDEO_URL)

        # find visible object in the middle of the page and scroll to it
        scroll_obj = wait.until(
            EC.presence_of_element_located((By.XPATH, MvideoLocators.NEWEST_TITLE)))
        driver.execute_script("arguments[0].scrollIntoView();", scroll_obj)

        # waiting for object to load
        wait.until(
            EC.presence_of_element_located((By.XPATH, MvideoLocators.TRENDS_BUTTON)))
        driver.find_element(By.XPATH, MvideoLocators.TRENDS_BUTTON).click()

        # find all items' urls in Trend block
        items = driver.find_elements(By.XPATH, MvideoLocators.TREND_URLS)
        items_url = [x.get_attribute('href') for x in items]

        goods = []
        for url in items_url:
            driver.get(url)

            # closing notification iframe
            try:
                driver.find_element(By.XPATH, '//iframe')
                driver.find_element(By.XPATH, '//a[@class="close"]').click()
            except NoSuchElementException:
                continue

            wait.until(EC.presence_of_element_located((By.XPATH, MvideoLocators.PRICE)))
            item = {
                'title': driver.find_element(By.XPATH, MvideoLocators.ITEM_TITLE).text,
                'link': url,
                'reviews': url + '/reviews',
                'code': driver.find_element(By.XPATH, MvideoLocators.CODE).text,
                'price': driver.find_element(By.XPATH, MvideoLocators.PRICE).text,
                'bonus': driver.find_element(By.XPATH, MvideoLocators.M_BONUS).text,
            }
            goods.append(item)
    return goods


if __name__ == '__main__':
    data = m_video()
    db_upload(data)
