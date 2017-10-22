#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write
import pyodbc, time
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120]

banners = [
    './/button[@class="cta widget-overlay-close"]',
    './/button[contains(@class, "cta widget-overlay-close")]',
    './/button[contains(@class, "close")]',
    './/div[@class="widget-query-group widget-query-occupancy"]',
    './/div/span[@class="title"][contains(text(), "Save an extra")]/following-sibling::span[@class="close-button"]',
    './/span[contains(@class, "close")]',
]

def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    return driver

def banner(driver):
    for banner in banners:
        try:
            element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, banner)))
            element.click()
        except:
            pass
                
def scroll_down(driver):
    c = 0
    while True:
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        c += 1
        try:
            driver.find_element_by_xpath('.//div[@class="info unavailable-info"]')
            break
        except:
            pass

        if c == 500:
            break

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
    driver = spider(url)
    
    banner(driver)

    ##### city
    city_element = './/input[@name="q-destination"]'
    city_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, city_element)))
    city_element.send_keys(city)
    time.sleep(5)
    city_element.click()
    
    banner(driver)

    ##### checkin
    checkin = datetime.now() + timedelta(date)
    checkinn = checkin.strftime('%m/%d/%Y')
    checkout = datetime.now() + timedelta(date + 3)
    checkoutt = checkout.strftime('%m/%d/%y')

    checkin_element = '//input[@name="q-localised-check-in"]'
    checkin_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, checkin_element)))
    checkin_element.clear()
    checkin_element.send_keys(checkinn)
    
    banner(driver)

    ##### checkout
    checkout_element = '//input[@name="q-localised-check-out"]'
    checkout_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, checkout_element)))
    checkout_element.clear()
    checkout_element.send_keys(checkoutt)
    
    banner(driver)

    ##### occupancy
    occupancy_element = './/select[@id="qf-0q-compact-occupancy"]/option[contains(text(), "1 room, 1 adult")]'
    occupancy_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, occupancy_element)))
    occupancy_element.click()

    ##### submit
    button_element = '//button[@type="submit"]'
    button_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, button_element)))
    button_element.click()
            
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    source = 'hotels.com'
    count = 0
    scroll_down(driver)
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
        #sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)

    print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)


if __name__ == '__main__':
    global conn
    global cur
    #conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    #cur = conn.cursor()
    url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    scrape_dates()
    #conn.close()


