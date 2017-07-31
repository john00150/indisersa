#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import spider, sql_write
import pyodbc, time
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120]

def scroll_down(driver):
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//span[contains(text(), "See more options")]'))
            element.click()
        except:
            break

def scrape_name(element):
    return WebDriverWait(element, 5).until(lambda element: element.find_element_by_xpath('.//a[@class="hotel-name"]').text.strip())

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

def scrape_dates():
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date) 

def scrape_city(url, city, date):
    driver = spider(url)
    element_1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@name="ajhoteles"]'))
    element_1.send_keys(city)

    if city == 'Guatemala City, Guatemala':
        element_2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[./strong[contains(text(), "Guatemala")]]'))
        element_2.click()

    if city == 'Antigua Guatemala, Guatemala':
        element_2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[contains(text(), "Antigua, Guatemala")]'))
        element_2.click()

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)
    element_3 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//input[@name="check-inH"]'))
    element_3.click()

    while True:
        try:
            element_4 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkin.strftime('%B'), checkin.day)))
            element_4.click()
            break
        except:
            next = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//span[@id="nextCalendar"]'))
            next.click()            

    while True:
        try:
            element_5 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "%s")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "%s")]' % (checkout.strftime('%B'), checkout.day)))
            element_5.click()
            break
        except:
            next = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//span[@id="nextCalendar"]'))
            next.click()  

    element_6 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//select[@name="num_adultos"]/option[contains(@value, "1")]'))
    element_6.click()
    element_7 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//button[@id="btnSubmitHotels"]'))
    element_7.click()
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    count = 0
    scroll_down(driver)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath('.//ul[@id="hotelList"]/li[contains(@class, "hotel-item")]') > 0)
    hotels = driver.find_elements_by_xpath('.//ul[@id="hotelList"]/li[contains(@class, "hotel-item")]')
    for hotel in hotels:
        count += 1
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = 0
        rating = scrape_rating(hotel)
        address = ''
        city = city.split(',')[0] 
        currency = 'USD'
        source = 'bestday.com'
        #if location not in city:
        #    continue

        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)

    print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.bestday.com/Hotels/'
    scrape_dates()
    conn.close()


