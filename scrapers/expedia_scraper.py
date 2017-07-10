#!/usr/bin/python
#encoding: utf8
from selenium.webdriver.common.keys import Keys
from processors import spider, sql_write
import time, re, pyodbc
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def get_name(element):
    name = element.find_element_by_xpath('./h3').text.strip()
    return name

def get_review(element):
    try:
        review = element.find_elements_by_xpath('.//li[contains(@class, "reviewCount")]/span')[1].text
        review = review.strip().strip('(').strip(')')
        return review
    except:
        return 0

def get_rating(element):
    try:
        rating = element.find_elements_by_xpath('.//li[@class="reviewOverall"]/span')[1].text.strip()
        return rating
    except:
        return 0

def get_actualprice(element):
    try:
        price = element.find_element_by_xpath('.//ul[@class="hotel-price"]/li[@data-automation="actual-price"]/a').text.strip()
        price = re.findall(r'([0-9$]+)', price)[0].strip('$')
    except:
        try:
            price = element.find_element_by_xpath('.//ul[@class="hotel-price"]/li[@data-automation="actual-price"]').text.strip()
            price = re.findall(r'([0-9$]+)', price)[0].strip('$')
        except:
            price = 0
    return price

def get_strikeprice(element):
    try:
        price = element.find_element_by_xpath('.//ul[@class="hotel-price"]/li[@data-automation="strike-price"]/a').text.strip()
        price = re.findall(r'([0-9$]+)', price)[0].strip('$')
    except:
        price = 0
    return price

def get_address(element):
    address = element.find_element_by_xpath('.//ul[@class="hotel-info"]/li[@class="neighborhood secondary"]').text.strip()
    try:
        phone = element.find_element_by_xpath('.//ul[@class="hotel-info"]/li[@class="phone secondary gt-mobile"]/span').text.strip()
    except:
        phone = ''
    line = '%s, %s.' % (address, phone)
    return line, address
    
def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x)

def scrape_city(url, city, index):
    driver = spider(url)

    driver.find_element_by_xpath('.//input[@id="hotel-destination-hlp"]').send_keys(city)
    driver.find_element_by_xpath('.//div[@class="hero-banner-box cf"]').click()
    time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        checkinn = checkin.strftime('%m/%d/%Y')
        checkout = datetime.now() + timedelta(days=2)
        checkoutt = checkout.strftime('%m/%d/%Y')
    if index == 1:
        checkin = datetime.now() + timedelta(days=120)
        checkinn = checkin.strftime('%m/%d/%Y')
        checkout = datetime.now() + timedelta(days=122)
        checkoutt = checkout.strftime('%m/%d/%Y')

    driver.find_element_by_xpath('.//input[@id="hotel-checkin-hlp"]').send_keys(checkinn)
    time.sleep(2)
    driver.find_element_by_xpath('.//input[@id="hotel-checkout-hlp"]').clear()
    driver.find_element_by_xpath('.//input[@id="hotel-checkout-hlp"]').send_keys(checkoutt)
    time.sleep(2)

    driver.find_element_by_xpath('.//select[contains(@class, "gcw-guests-field")]/option[contains(text(), "1 adult")]').click()
    time.sleep(2)

    driver.find_element_by_xpath('.//section[@id="section-hotel-tab-hlp"]/form').find_element_by_xpath('.//button[@type="submit"]').click()
    time.sleep(2)
    scrape_hotels(driver, city, checkin.date(), checkout.date())

def scrape_hotels(driver, city, checkin, checkout):
    count = 0
    while True:
        time.sleep(5)
        hotels = driver.find_elements_by_xpath('.//div[@id="resultsContainer"]/section/article')
        for hotel in hotels:
            new_price = get_actualprice(hotel)
            old_price = get_strikeprice(hotel)
            name = get_name(hotel)
            review = get_review(hotel)
            rating = get_rating(hotel)
            address, location = get_address(hotel)
            address = address
            city = city.split(',')[0]
            currency = 'USD'
            source = 'expedia.com'
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, location)
            count += 1   
 
        try:       
            next = driver.find_element_by_xpath('.//button[@class="pagination-next"]/abbr')
            next.click()
        except:            
            driver.quit()
            print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)
            break

if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.expedia.com/Hotels'
    scrape_cities(url)
    conn.close()

