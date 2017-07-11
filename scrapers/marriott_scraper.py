#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_write, spider
import time, pyodbc
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
#    'Antigua Guatemala, Guatemala',
]

def scrape_name(element):
    return element.find_element_by_xpath('.//h3[@class="m-result-hotel-title"]/a').get_attribute('title')

def scrape_address(element):
    return element.find_element_by_xpath('.//p[contains(@class, "m-hotel-address")]').text.strip()

def scrape_location(element):
    return element.find_element_by_xpath('.//p[@class="m-hotel-distance t-font-sm"]').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//div[@class="m-pricing-block"]/p').text.strip()
        old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//div[contains(@class, "l-hotel-rating")]/a/span').text.strip()
    except:
        return 0

def scrape_review(element):
    return 0

def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    driver.find_elements_by_xpath('.//input[@name="destinationAddress.destination"]')[1].send_keys(city)
    time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        day = checkin.strftime('%A')[:3]
        month = checkin.strftime('%B')[:3]
        str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)

        checkout = datetime.now() + timedelta(days=2)
        day2 = checkout.strftime('%A')[:3]
        month2 = checkout.strftime('%B')[:3]
        str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    if index == 1:
        checkin = datetime.now() + timedelta(days=120)
        day = checkin.strftime('%A')[:3]
        month = checkin.strftime('%B')[:3]
        str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)

        checkout = datetime.now() + timedelta(days=122)
        day2 = checkout.strftime('%A')[:3]
        month2 = checkout.strftime('%B')[:3]
        str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].click()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].clear()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].send_keys(str1)
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-out"]')[1].clear()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-out"]')[1].send_keys(str2)
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].click()
    time.sleep(2)
    driver.find_elements_by_xpath('.//button[@title="Find"]')[1].click()
    time.sleep(2)
    scrape_hotels(driver, city, checkin, checkout)
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    count = 0
    checkin = checkin.date()
    checkout = checkout.date()
    hotels = driver.find_elements_by_xpath('.//div[contains(@class, "merch-property-records")]')
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = scrape_review(hotel)
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        checkin = checkin
        checkout = checkout
        city = city.split(',')[0]
        location = scrape_location(hotel)     
        source = 'marriott.com'
        currency = 'USD'
        count += 1

        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, location)

    print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)

def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)
    return driver


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'http://www.marriott.com/search/default.mi'
    scrape_cities(url)
    conn.close()


