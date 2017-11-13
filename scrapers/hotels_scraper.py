#encoding: utf8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import _db, spider, close_banner, scroll_down
import time
from datetime import datetime, timedelta
from settings import cities, dates



banners = [
    './/button[@class="cta widget-overlay-close"]',
    './/button[contains(@class, "cta widget-overlay-close")]',
    './/button[contains(@class, "close")]',
    './/div[@class="widget-query-group widget-query-occupancy"]',
    './/div/span[@class="title"][contains(text(), "Save an extra")]/following-sibling::span[@class="close-button"]',
    './/span[contains(@class, "close")]',
    './/span[contains(@class, "close-icon")]',
    './/button[contains(@class, "cta")]'
]

def scrape_address(driver):
    address = './/div[@class="contact"]/p'
    elements = driver.find_elements_by_xpath(address)
    line = ''
    elements_1 = ' '.join([x.text for x in elements[0].find_elements_by_xpath('./span')])
    elements_2 = elements[1].text
    line = '%s, %s.' % (elements_1, elements_2)
    return line

def scrape_price(element):
    try:
        new_price = './/span[@class="old-price-cont"]/ins'
        old_price = './/span[@class="old-price-cont"]/del'
        new_price = element.find_element_by_xpath(new_price).text.strip().strip('$').strip()
        old_price = element.find_element_by_xpath(old_price).text.strip().strip('$').strip()
        return new_price, old_price
    except:
        try:
            new_price = './/b[@class="fewRoomsLeft"]'
            new_price = element.find_element_by_xpath(new_price).text.strip().strip('$').strip()
            old_price = 0
            return new_price, old_price
        except:
            try:
                old_price = './/div[@class="price"]/a/b'
                old_price = element.find_element_by_xpath(old_price).text.strip().strip('$').strip()
                new_price = old_price
                return new_price, old_price
            except:
                return 0, 0

def scrape_rating(element):
    try:
        rating = './/div[contains(@class, "guest-rating")]'
        rating = element.find_element_by_xpath(rating).text.strip()
        return rating
    except:
        return 0

def scrape_review(element):
    try:
        review = './/div[@class="guest-reviews-link"]/a/span[@class="full-view"]'
        review = element.find_element_by_xpath(review).text
        return review
    except:
        return 0

def scrape_dates():
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date) 

def scrape_city(url, city, date):
    driver = spider.chrome(url)
    
    close_banner(driver, banners)

    ##### city
    city_element = './/input[@name="q-destination"]'
    city_element = process_element.visibility(driver, city_element, 10)
    city_element.send_keys(city)
    time.sleep(5)
    city_element.click()
    
    close_banner(driver, banners)

    ##### checkin
    checkin = datetime.now() + timedelta(date)
    checkinn = checkin.strftime('%m/%d/%Y')
    checkin_element = '//input[@name="q-localised-check-in"]'
    checkin_element = process_element.presence(driver, checkin_element, 10)
    checkin_element.clear()
    checkin_element.send_keys(checkinn)
    
    close_banner(driver, banners)

    ##### checkout
    checkout = datetime.now() + timedelta(date + 3)
    checkoutt = checkout.strftime('%m/%d/%y')
    checkout_element = '//input[@name="q-localised-check-out"]'
    checkout_element = process_element.presence(driver, checkout_element, 10)
    checkout_element.clear()
    checkout_element.send_keys(checkoutt)
    
    close_banner(driver, banners)

    ##### occupancy
    occupancy_element = './/select[@id="qf-0q-compact-occupancy"]/option[contains(text(), "1 room, 1 adult")]'
    occupancy_element = process_element.visibility(driver, occupancy_element, 10)
    occupancy_element.click()

    close_banner(driver, banners)

    ##### submit
    button_element = './/button[contains(@type, "submit")]'
    button_element = process_element.visibility(driver, button_element, 10)
    button_element.click()
            
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    source = 'hotels.com'
    count = 0
    
    scroll_down.range(driver, 500, 0.5)
    
    hotel_elms = './/ol[contains(@class, "listings")]/li[@class="hotel"]'
    hotel_elements = driver.find_elements_by_xpath(hotel_elms)
    for hotel in hotel_elements:
        name = hotel.get_attribute('data-title')
        new_price, old_price = scrape_price(hotel)
        review = scrape_review(hotel)
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        currency = 'USD'
        city = city.split(',')[0]
        
        count += 1
        _db.sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)

    print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)


if __name__ == '__main__':
    global conn
    global cur
    conn, cur = _db.connect()
    url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    
    scrape_dates()
    
    conn.close()


