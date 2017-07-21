#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write
import pyodbc, time
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def banner(driver):
    try:
        driver.find_element_by_xpath('.//body').click()
    except:
        pass 

def spider(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver 

def scroll_down(driver):
    for x in range(300):
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.4)

def scrape_name(element):
    return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//span[@class="sr-hotel__name"]').text) 

def scrape_address(element):
    return element.find_element_by_xpath('.//div[@class="address"]/a').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/strong/b').text.strip().strip('GTQ').strip().replace(',', '')
        new_price = int(new_price) / 3
        try:
            old_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span').text.strip().strip('GTQ').strip().replace(',', '')
            old_price = int(old_price) / 3
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//span[@itemprop="ratingValue"]').text.strip()
    except:
        return 0

def scrape_review(element):
    try:
        review = element.find_element_by_xpath('.//span[@class="score_from_number_of_reviews"]').text
        return review
    except:
        return 0

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city) 

def scrape_city(url, city):
    driver = spider(url)
    element_1 = driver.find_element_by_xpath('.//input[@id="ss"][@class="c-autocomplete__input sb-searchbox__input sb-destination__input"]')
    element_1.send_keys(city)
    time.sleep(5)
    if city == 'Guatemala City, Guatemala':
        element_2 = driver.find_element_by_xpath('.//b[@class="search_hl_name"][contains(text(), "Guatemala (Guatemala City)")]')
        element_2.click()
        time.sleep(2)
    if city == 'Antigua Guatemala, Guatemala':
        element_2 = driver.find_element_by_xpath('.//b[@class="search_hl_name"][contains(text(), "Antigua Guatemala")]')
        element_2.click()
        time.sleep(2)

    checkin = datetime.now() + timedelta(days=15)
    checkout = datetime.now() + timedelta(days=18)
    str1 = '%s %s' % (checkin.strftime('%B'), checkin.year)
    str2 = '%s %s' % (checkout.strftime('%B'), checkout.year)
    element_3 = driver.find_element_by_xpath('.//div[@data-mode="checkin"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str1, checkin.day))
    element_3.click()
    time.sleep(2)
    element_4 = driver.find_element_by_xpath('.//div[@data-placeholder="Check-out Date"]')
    element_4.click()
    time.sleep(2)
    element_5 = driver.find_element_by_xpath('.//div[@data-mode="checkout"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str2, checkout.day))
    element_5.click()
    time.sleep(2)

    element_6 = driver.find_element_by_xpath('.//select[@name="group_adults"]/option[contains(@value, "1")]')
    element_6.click()
    time.sleep(2)
    element_7 = driver.find_element_by_xpath('//button[@type="submit"]')
    element_7.click()
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))
    driver.quit()

def get_pages(driver, city, checkin, checkout):
    count = 0
    while True:
        scroll_down(driver)
        WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_xpath('.//div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]')) > 0)
        hotels = driver.find_elements_by_xpath('.//div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]')
        for hotel in hotels:
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'booking.com'
            count += 1
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
         
        try:
            _next = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//a[contains(@class, "paging-next")]'))
            _next.click()
        except:
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s' % (source, city, count, checkin, checkout)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.booking.com/'
    scrape_cities(url)
    conn.close()


