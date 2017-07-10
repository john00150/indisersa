#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_write, spider
import time, pyodbc
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def scrape_name(element):
    return element.find_element_by_xpath('.//div[@class="innername"]/a').text.strip()

def scrape_address(element):
    return element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[0].strip()

def scrape_location(element):
    return element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[1].strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//td[@class="rateamount"]').text.strip()
        old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//img[@class="rating_circles"]').get_attribute('title')
    except:
        return 0

def scrape_review(element):
    return element.find_element_by_xpath('.//a[@class="ratingLink"]').text.strip()

def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[@name="city"]').send_keys(city)
    time.sleep(2)
    driver.find_element_by_xpath('.//input[@id="checkinDate"]').click()
    time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        checkout = datetime.now() + timedelta(days=2)

    if index == 1:
        checkin = datetime.now() + timedelta(days=120)
        checkout = datetime.now() + timedelta(days=122)
        for x in range(4):
            driver.find_element_by_xpath('.//a[contains(@class, "ui-datepicker-next")]').click()
            time.sleep(1)

    driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//input[@id="checkoutDate"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//a[contains(@title, "Search Destination")]').click()
    time.sleep(10)
    scrape_hotels(driver, city, checkin, checkout)
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    checkin = checkin.date()
    checkout = checkout.date()
    new_price, old_price = scrape_price(driver)
    name = scrape_name(driver)
    review = scrape_review(driver)
    rating = scrape_rating(driver)
    address = scrape_address(driver)
    city = city.split(',')[0]
    location = scrape_location(driver)     
    source = 'radisson.com'
    currency = 'USD'
    #sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, location)
    #print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)
    print name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, location


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.radisson.com/'
    scrape_cities(url)
    conn.close()


