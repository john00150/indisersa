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

def banner(driver):
    try:
        driver.find_element_by_xpath('.//div/span[@class="title"][contains(text(), "Save an extra")]/following-sibling::span[@class="close-button"]').click()
    except:
        pass 
    try:
        driver.find_element_by_xpath('.//button[@class="cta widget-overlay-close"]').click()
    except:
        pass  

def scroll_down(driver):
    while True:
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1)
        try:
            driver.find_element_by_xpath('.//div[@class="info unavailable-info"]')
            break
        except:
            pass

def scrape_address(driver):
    elements = driver.find_elements_by_xpath('.//div[@class="contact"]/p')
    line = ''
    elements_1 = ' '.join([x.text for x in elements[0].find_elements_by_xpath('./span')])
    elements_2 = elements[1].text
    line = '%s, %s.' % (elements_1, elements_2)
    return line

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//span[@class="old-price-cont"]/ins').text.strip().strip('$').strip()
        old_price = element.find_element_by_xpath('.//span[@class="old-price-cont"]/del').text.strip().strip('$').strip()
        return new_price, old_price
    except:
        try:
            new_price = element.find_element_by_xpath('.//b[@class="fewRoomsLeft"]').text.strip().strip('$').strip()
            old_price = 0
            return new_price, old_price
        except:
            try:
                old_price = element.find_element_by_xpath('.//div[@class="price"]/a/b').text.strip().strip('$').strip()
                new_price = old_price
                return new_price, old_price
            except:
                return 0, 0

def scrape_rating(element):
    try:
        rating = element.find_element_by_xpath('.//div[contains(@class, "guest-rating")]').text.strip()
        return rating
    except:
        return 0

def scrape_review(element):
    try:
        review = element.find_element_by_xpath('.//div[@class="guest-reviews-link"]/a/span[@class="full-view"]').text
        return review
    except:
        return 0

def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    banner(driver)
    element = driver.find_element_by_xpath('.//input[@name="q-destination"]')
    element.send_keys(city)
    element.click()
    banner(driver)
    time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        checkinn = checkin.strftime('%m/%d/%Y')

        checkout = datetime.now() + timedelta(days=2)
        checkoutt = checkout.strftime('%m/%d/%y')

    if index == 1:
        checkin = datetime.now() + timedelta(days=120)
        checkinn = checkin.strftime('%m/%d/%Y')

        checkout = datetime.now() + timedelta(days=122)
        checkoutt = checkout.strftime('%m/%d/%y')

    checkin_element = driver.find_element_by_xpath('//input[@name="q-localised-check-in"]')
    checkin_element.send_keys(checkinn)
    banner(driver)
    time.sleep(2)
    checkout_element = driver.find_element_by_xpath('//input[@name="q-localised-check-out"]')
    checkout_element.clear()
    checkout_element.send_keys(checkoutt)
    banner(driver)
    try:
        driver.find_element_by_xpath('.//div[@class="widget-query-group widget-query-occupancy"]').click()
    except:
        pass
    time.sleep(2)

    occupancy_element = driver.find_element_by_xpath('.//select[@id="qf-0q-compact-occupancy"]/option[contains(text(), "1 room, 1 adult")]')
    occupancy_element.click()
    time.sleep(2)

    element = driver.find_element_by_xpath('//button[@type="submit"]')
    element.click()
    time.sleep(2)
    scrape_hotels(driver, city, checkin, checkout)

    driver.quit()

def scrape_hotels(driver, city, checkin, checkout):
    count = 0
    scroll_down(driver)
    hotels = driver.find_elements_by_xpath('.//ol[contains(@class, "listings")]/li[contains(@class, "hotel")]')
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = hotel.get_attribute('data-title')
        review = scrape_review(hotel)
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        currency = 'USD'
        city = city.split(',')[0]
        source = 'hotels.com'
        location = ''
        if city not in address:
            continue
        count += 1
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin.date(), checkout.date(), city, currency, source, location)

    print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin.date(), checkout.date())


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    scrape_cities(url)
    conn.close()


