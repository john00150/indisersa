#encoding: utf8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import _db, spider, scroll_down
import time
from datetime import datetime, timedelta
from settings import cities, dates


url = 'https://www.bestday.com/Hotels/'
currency = 'USD'
source = 'bestday.com'

def scrape_name(element):
    return WebDriverWait(element, 5).until(lambda element: element.find_element_by_xpath('.//a[@class="hotel-name"]').text.strip())

def scrape_address(element):
    address = './/div[@class="details"]/a/span'
    address = element.find_element_by_xpath(address).text.strip()
    return address

def scrape_price(element):
    new_price = './/span[@class="currency"]/span[@class="currency-price"]'
    old_price = './/span[@class="currency-before"]/span[@class="currency-before"]/span[@class="currency-price"]'
    try:
        new_price = element.find_element_by_xpath(new_price).text.strip().strip('us$').strip()
        try:
            old_price = element.find_element_by_xpath(old_price).text.strip().strip('us$').strip()
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    review = './/span[@class="reviews"]'
    try:
        return element.find_element_by_xpath(review).text.strip()
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
    driver = spider.chrome(url)
    
    input_el = './/input[@name="ajhoteles"]'
    input_element = process_elements.presence(driver, input_el, 10)
    input_element.send_keys(city)

    if city == 'Guatemala City, Guatemala':
        city_el = './/ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[./strong[contains(text(), "Guatemala")]]'
        city_element = process_elements.visibility(driver, city_el, 10)
        city_element.click()

    else:
        city_el = './/ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[contains(text(), "Antigua, Guatemala")]'
        city_element = process_elements.visibility(driver, city_el, 10)
        city_element.click()

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)
    element_3 = '//input[@name="check-inH"]'
    element_3 = process_elements.visibility(driver, element_3, 10)
    element_3.click()

    checkin_el = './/div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "{}")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "{}")]'.format(checkin.strftime('%B'), checkin.day)
    checkout_el = './/div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(), "{}")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "{}")]'.format(checkout.strftime('%B'), checkout.day)
    next_el = '//span[@id="nextCalendar"]'

    while True:
        try:
            checkin_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, checkin_el)))
            checkin_element.click()
            break
        except Exception, e:
            next_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, next_el)))
            next_element.click()

    time.sleep(5)            

    while True:
        try:
            checkout_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, checkout_el)))
            checkout_element.click()
            break
        except:
            next_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, next_el)))
            next_element.click()

    time.sleep(5)  

    occupancy_el = './/select[@name="num_adultos"]/option[contains(@value, "1")]'
    occupancy_element = process_elements.visibility(driver, occupancy_el, 10)
    occupancy_element.click()

    button_el = './/button[@id="btnSubmitHotels"]'
    button_element = process_elements.visibility(driver, button_el, 10)
    button_element.click()

    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    count = 0

    scrolldown_el = './/span[contains(text(), "See more options")]'
    try:
        scroll_down.click_element(driver, 400, scrolldown_el, 0.5)
    except:
        pass

    hotel_elms = './/ul[@id="hotelList"]/li[contains(@class, "hotel-item")]'
    hotel_elements = driver.find_elements_by_xpath(hotel_elms)
    for hotel in hotel_elements:
        new_price, old_price = scrape_price(hotel)
        name = scrape_name(hotel)
        review = 0
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        city = city.split(',')[0] 

        if address not in city:
            continue

        count += 1
        _db.sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)

    print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)


if __name__ == '__main__':
    global conn
    global cur
    
    conn, cur = _db.connect()

    scrape_dates()

    conn.close()


