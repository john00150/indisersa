#!/usr/bin/python
#encoding: utf8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from processors import spider, sql_write
import re, pyodbc, time
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def get_name(element):
    return element.find_element_by_xpath('./h3').text.strip()

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

def banner(driver):
    try:
        banner = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//div[@class="hero-banner-box cf"]'))
        banner.click()
    except:
        pass    

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city) 

def scrape_city(url, city):
    driver = spider(url)
    element_1 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//input[@id="hotel-destination-hlp"]'))
    element_1.send_keys(city)
    banner(driver)

    checkin = datetime.now() + timedelta(days=15)
    checkinn = checkin.strftime('%m/%d/%Y')
    checkout = datetime.now() + timedelta(days=18)
    checkoutt = checkout.strftime('%m/%d/%Y')

    element_2 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//input[@id="hotel-checkin-hlp"]'))
    element_2.send_keys(checkinn)
    element_3 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//input[@id="hotel-checkout-hlp"]'))
    element_3.clear()
    element_3.send_keys(checkoutt)

    element_4 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//select[contains(@class, "gcw-guests-field")]/option[contains(text(), "1 adult")]'))
    element_4.click()

    element_5 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//section[@id="section-hotel-tab-hlp"]/form').find_element_by_xpath('.//button[@type="submit"]'))
    element_5.click()
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))

def scrape_hotels(driver, city, checkin, checkout):
    count = 0
    while True:
        WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_xpath('.//div[@id="resultsContainer"]/section/article')) > 0)
        hotels = driver.find_elements_by_xpath('.//div[@id="resultsContainer"]/section/article')
        for hotel in hotels:
            count += 1
            name = get_name(hotel)
            new_price = get_actualprice(hotel)
            old_price = get_strikeprice(hotel)
            review = get_review(hotel)
            rating = get_rating(hotel)
            address, location = get_address(hotel)
            city = city.split(',')[0]
            currency = 'USD'
            source = 'expedia.com'
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count)   
 
        try:       
            _next = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//button[@class="pagination-next"]/abbr'))
            _next.click()
            time.sleep(10)
        except:            
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s' % (source, city, count, checkin, checkout)
            break

if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.expedia.com/Hotels'
    scrape_cities(url)
    conn.close()

