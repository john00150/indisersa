#encoding: utf8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import _db, spider, scroll_down, process_elements
import time, os, traceback
from datetime import datetime, timedelta
from settings import cities, dates


def scrape_address(element):
    try:
        return element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_location")]').text
    except:
        return ''

def scrape_name(element):
    return element.find_element_by_xpath('.//a[contains(@data-ceid, "searchresult_hotelname")]').get_attribute('title')

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_price")]').text.strip().strip('Q').strip().replace(',', '')
        new_price = int(new_price) / 3
        try:
            old_price = element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_wasPrice")]').text.strip().strip('Q').strip().replace(',', '')
            old_price = int(old_price) / 3
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//p[@class="hc_hotel_userRating"]/a').text.strip()
    except:
        return 0

def scrape_review(element):
    try:
        return element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_numberOfReviews")]/span').text.strip()
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

    ##### city
    city_el1 = './/div[@class="hcsb_citySearchWrapper"]/input'
    city_element1 = process_elements.presence(driver, city_el1, 10)
    city_element1.send_keys(city)

    city_el2 = './/ul[@id="ui-id-1"]/li' 
    city_element2 = process_elements.visibility(driver, city_el2, 10)
    city_element2.click()
    
    ##### checkin
    checkin = datetime.now() + timedelta(date)
    checkin_year_month = '%s-%s' % (checkin.year, checkin.month)

    checkin_el1 = '//select[@class="hcsb_checkinMonth"]/option[@value="{}"]'.format(checkin_year_month)
    checkin_element1 = process_elements.visibility(driver, checkin_el1, 10)
    checkin_element1.click()
    
    checkin_el2 = '//select[@class="hcsb_checkinDay"]/option[@value="{}"]'.format(checkin.day)
    checkin_element2 = process_elements.visibility(driver, checkin_el2, 10)
    checkin_element2.click()

    checkin_el3 = './/div[contains(@class, "hcsb_checkinDateWrapper")]'
    checkin_element3 = process_elements.visibility(driver, checkin_el3, 10)
    checkin_element3.click()

    ##### checkout
    checkout = datetime.now() + timedelta(date + 3)
    checkout_year_month = '%s-%s' % (checkout.year, checkout.month)

    checkout_el1 = '//select[@class="hcsb_checkoutMonth"]/option[@value="{}"]'.format(checkout_year_month)
    checkout_element1 = process_elements.visibility(driver, checkout_el1, 10)
    checkout_element1.click()
    
    checkout_el2 = '//select[@class="hcsb_checkoutDay"]/option[@value="{}"]'.format(checkout.day)
    checkout_element2 = process_elements.visibility(driver, checkout_el2, 10)
    checkout_element2.click()

    checkout_el3 = './/div[contains(@class, "hcsb_checkinDateWrapper")]'
    checkout_element3 = process_elements.visibility(driver, checkout_el3, 10)
    checkout_element3.click()

    ##### occupancy
    occupancy_el = './/select[@class="hcsb_guests"]/option[@value="1-1"]'
    occupancy_element = process_elements.visibility(driver, occupancy_el, 10)
    occupancy_element.click()

    ##### submit
    submit_el = '//a[@class="hcsb_searchButton"]'
    submit_element = process_elements.visibility(driver, submit_el, 10)
    submit_element.click()

    WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to_window(driver.window_handles[1])

    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

def scrape_hotels(driver, city, checkin, checkout, date):
    _next = './/a[contains(text(), "Next")]'
    hotels_el = './/div[@class="hc_sr_summary"]/div[@class="hc_sri hc_m_v4"]'
    count = 0
    while True:
        time.sleep(20)
        hotels = driver.find_elements_by_xpath(hotels_el)

        for hotel in hotels:
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'book-hotel-beds.com'
            count += 1
            _db.sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
        time.sleep(10)

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            page_next = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, _next)))
            page_next.click()
        except Exception, e:
            print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)
            driver.quit()
            break


if __name__ == '__main__':
    global conn
    global cur

    conn, cur = _db.connect()
    url = 'http://www.book-hotel-beds.com/'
    
    scrape_dates()

    conn.close()


