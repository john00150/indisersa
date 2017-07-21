#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write
import pyodbc
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
#    'Antigua Guatemala, Guatemala',
]

def scrape_name(element):
    return WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//h3[@class="m-result-hotel-title"]/a').get_attribute('title'))

def scrape_address(element):
    return WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//p[contains(@class, "m-hotel-address")]').text.strip())

def scrape_location(element):
    return WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//p[@class="m-hotel-distance t-font-sm"]').text.strip())

def scrape_price(element):
    try:
        new_price = WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//div[@class="m-pricing-block"]/p').text.strip())
        old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//div[contains(@class, "l-hotel-rating")]/a/span').text.strip())
    except:
        return 0

def scrape_review(element):
    return 0

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city) 

def scrape_city(url, city):
    driver = spider(url)
    destination_element = WebDriverWait(driver, 20).until(lambda driver: driver.find_elements_by_xpath('.//input[@name="destinationAddress.destination"]')[1])
    destination_element.send_keys(city)

    checkin = datetime.now() + timedelta(days=15)
    day = checkin.strftime('%A')[:3]
    month = checkin.strftime('%B')[:3]
    str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)
    checkout = datetime.now() + timedelta(days=18)
    day2 = checkout.strftime('%A')[:3]
    month2 = checkout.strftime('%B')[:3]
    str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    checkin_element = WebDriverWait(driver, 20).until(lambda driver: driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1])
    checkin_element.click()
    checkin_element.clear()
    checkin_element.send_keys(str1)
    checkout_element = WebDriverWait(driver, 20).until(lambda driver: driver.find_elements_by_xpath('.//input[@placeholder="Check-out"]')[1])
    checkout_element.clear()
    checkout_element.send_keys(str2)
    checkin_element.click()
    button_element = WebDriverWait(driver, 20).until(lambda driver: driver.find_elements_by_xpath('.//button[@title="Find"]')[1])
    button_element.click()
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    count = 0
    hotels = WebDriverWait(driver, 20).until(lambda driver: driver.find_elements_by_xpath('.//div[contains(@class, "merch-property-records")]'))
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = scrape_review(hotel)
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        city = city.split(',')[0]
        source = 'marriott.com'
        currency = 'USD'
        count += 1
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)

    print '%s, %s, %s hotels, checkin %s, checkout %s' % (source, city, count, checkin, checkout)

def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    return driver


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'http://www.marriott.com/hotels/travel/guacy-courtyard-guatemala-city/'
    scrape_cities(url)
    conn.close()


