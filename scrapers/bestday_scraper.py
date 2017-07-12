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
        new_price = element.find_element_by_xpath('.//span[@class="currency"]/span[@class="currency-price"]').text.strip().strip('us$').strip()
        try:
            old_price = element.find_element_by_xpath('.//span[@class="currency-before"]/span[@class="currency-before"]/span[@class="currency-price"]').text.strip().strip('us$').strip()
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//span[@class="reviews"]').text.strip()
    except:
        return 0

def scrape_review(element):
    pass

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city) 

def scrape_city(url, city):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[@name="ajhoteles"]').send_keys(city)
    time.sleep(2)

    if city == 'Guatemala City, Guatemala':
        driver.find_elements_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[./strong[contains(text(), "Guatemala")]]')[0].click()
        time.sleep(2)

    if city == 'Antigua Guatemala, Guatemala':
        driver.find_elements_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[contains(text(), "Antigua, Guatemala")]')[0].click()
        time.sleep(2)

    checkin = datetime.now() + timedelta(days=15)
    checkout = datetime.now() + timedelta(days=18)
    driver.find_element_by_xpath('//input[@name="check-inH"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkin.strftime('%B'), checkin.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkout.strftime('%B'), checkout.day)).click()
    time.sleep(2)

    driver.find_element_by_xpath('.//select[@name="num_adultos"]/option[contains(@value, "1")]').click()
    time.sleep(2)
    driver.find_element_by_xpath('.//button[@id="btnSubmitHotels"]').click()
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    time.sleep(10)
    count = 0
    scroll_down(driver)
    hotels = driver.find_elements_by_xpath('.//ul[@id="hotelList"]/li[contains(@class, "hotel-item")]')
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = 0
        rating = scrape_rating(hotel)
        address = ''
        city = city.split(',')[0] 
        currency = 'USD'
        source = 'bestday.com'
        #location = scrape_address(hotel)
        #if location not in city:
        #    continue

        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
        count += 1

    print '%s, %s, %s hotels, checkin %s, checkout %s' % (source, city, count, checkin, checkout)


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.bestday.com/Hotels/'
    scrape_cities(url)
    conn.close()


