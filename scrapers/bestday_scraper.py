#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import spider, sql_write
import time, pyodbc
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def scroll_down(driver):
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath('.//span[contains(text(), "See more options")]').click()
            time.sleep(5)
        except:
            break

def scrape_name(element):
    return element.find_element_by_xpath('.//a[@class="hotel-name"]').text.strip()

def scrape_address(element):
    return element.find_element_by_xpath('.//div[@class="details"]/a/span').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//span[@class="currency"]/span[@class="currency-price"]').text.strip()
        try:
            old_price = element.find_element_by_xpath('.//span[@class="currency-before"]/span[@class="currency-before"]/span[@class="currency-price"]').text.strip()
        except:
            old_price = ''
        return new_price, old_price
    except:
        return '', ''

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//span[@class="reviews"]').text.strip()
    except:
        return ''

def scrape_review(element):
    pass

def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[@name="ajhoteles"]').send_keys(city)
    time.sleep(2)

    if city == 'Guatemala City, Guatemala':
        driver.find_elements_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[./strong[contains(text(), "Guatemala")]]')[0].click()
        time.sleep(2)

    if city == 'Antigua Guatemala, Guatemala':
        driver.find_elements_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[contains(text(), "Antigua, Guatemala")]')[0].click()
        time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        delta = timedelta(days=2)
        checkout = datetime.now() + delta

        driver.find_element_by_xpath('//input[@name="check-inH"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('.//button[contains(text(), "Today")]').click()
        time.sleep(2)
        driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkin.strftime('%B'), checkin.day)).click()
        time.sleep(2)
        driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkout.strftime('%B'), checkout.day)).click()
        time.sleep(2)

    if index == 1:
        delta_1 = timedelta(days=120)
        checkin = datetime.now() + delta_1

        delta_2 = timedelta(days=122)
        checkout = datetime.now() + delta_2

        driver.find_element_by_xpath('//input[@name="check-inH"]').click()
        for x in range(4):
            driver.find_element_by_xpath('.//span[@id="nextCalendar"]').click()
            time.sleep(1)

        driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkin.strftime('%B'), checkin.day)).click()
        time.sleep(2)
        driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkout.strftime('%B'), checkout.day)).click()
        time.sleep(2)

    driver.find_element_by_xpath('.//select[@name="num_adultos"]/option[contains(@value, "1")]').click()
    time.sleep(2)
    driver.find_element_by_xpath('.//button[@id="btnSubmitHotels"]').click()
    scrape_hotels(driver, city, checkin, checkout)
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    time.sleep(10)
    checkin = checkin.date()
    checkout = checkout.date()
    count = 0
    scroll_down(driver)
    hotels = driver.find_elements_by_xpath('.//ul[@id="hotelList"]/li[contains(@class, "hotel-item")]')
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = ''
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        checkin = checkin
        checkout = checkout
        city = city.split(',')[0] 
        currency = 'GTQ'
        source = 'bestday.com'
        if address not in city:
            continue
        if len(new_price) == 0 and len(old_price) == 0:
            continue

        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
        count += 1

    print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.bestday.com/Hotels/'
    scrape_cities(url)
    conn.close()


