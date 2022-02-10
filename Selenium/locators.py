class MvideoLocators:
    NEWEST_TITLE = '//h2[contains(text(), "Новинки")]'
    TRENDS_BUTTON = '//span[contains(text(), "В тренде")]'
    TRENDS_BLOCK = '//div/mvid-shelf-group//mvid-product-cards-group'
    ITEM_TITLE = '//h1'
    TREND_URLS = TRENDS_BLOCK + '//div[contains(@class, "product-mini-card__name")]/div/a'
    PRICE = '//div[contains(@class,"personal-price")]/span[@class="price__main-value"]'
    CODE = '//div[@class = "product-code-container"]/span[2]'
    M_BONUS = '//span[@class = "mbonus-block__value"]'
