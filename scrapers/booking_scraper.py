#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from processors import *
import pyodbc, time, os, traceback
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120] 

banners = [
    './/div[contains(@class, "close")]',
]


def scroll_down(driver):
    time.sleep(5)
    try:
        elms = './/td[contains(@class, "roomPrice sr_discount")]/div/strong[contains(@class, "price scarcity_color")]/b'
        elements = driver.find_elements_by_xpath(elms)
        while True:
            driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)
            elements_2 = [e for e in elements if len(e.text.strip())!=0]
            if len(elements) == len(elements_2):
                break
    except:
        for x in range(400):
            driver.find_element_by_xpath('.//body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)

def scrape_name(element): 
    name_el = './/span[contains(@class, "sr-hotel__name")]'
    name_element = element.find_element_by_xpath(name_el).text
    return name_element

def scrape_address(element):
    address_el = './/div[@class="address"]/a'
    address_element = element.find_element_by_xpath(address_el).text.strip()
    return element

def scrape_price(element):
    try:
        new_price = './/td[contains(@class, "roomPrice sr_discount")]/div/strong/b'
        new_price = element.find_element_by_xpath(new_price).text.strip().strip('GTQ').strip().replace(',', '')
        try:
            old_price = './/td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span'
            old_price = element.find_element_by_xpath(old_price).text.strip().strip('GTQ').strip().replace(',', '')
        except:
            old_price = 0
        return int(new_price)/3, int(old_price)/3
    except:
        return 0, 0

def scrape_rating(element):
    try:
        rating = './/span[@itemprop="ratingValue"]'
        rating = element.find_element_by_xpath(rating).text.strip()
        return rating
    except:
        return 0

def scrape_review(element):
    try:
        review ='.//span[@class="score_from_number_of_reviews"]' 
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
    
    city_element_before = './/input[@id="ss"]'
    city_element_before = process_elements.visibility(driver, city_element_before, 15)
    city_element_before.send_keys(city)

    city_element_after = './/li[contains(@class, "autocomplete")]'
    city_element_after = process_elements.visibility(driver, city_element_after, 15)
    city_element_after.click()

    #####
    checkin_checkout_el = './/table[contains(@class, "c2-month-table")][./thead/tr/th[contains(text(), "{}")]]/tbody/tr/td/span[contains(text(), "{}")]'
    further_el = './/div[contains(@class, "c2-button-further")]'

    #####
    checkin = datetime.now() + timedelta(date)
    year = checkin.strftime('%Y')
    month = checkin.strftime('%B')
    month_year = '{} {}'.format(month, year)
    day = checkin.strftime('%d')
    checkin_el = checkin_checkout_el.format(month_year, day)    

    while True:
        try:
            element = process_elements.visibility(driver, checkin_el, 10)
            element.click()
            break
        except Exception, e:
            further_element = process_elements.visibility(driver, further_el, 10)
            further_element.click()

    checkout_element = './/div[@data-placeholder="Check-out Date"]'
    checkout_element = process_elements.visibility(driver, checkout_element, 10)
    checkout_element.click()

    ##### checkout
    checkout = datetime.now() + timedelta(date + 3)
    year = checkout.strftime('%Y')
    month = checkout.strftime('%B')
    month_year = '{} {}'.format(month, year)
    day = checkout.strftime('%d')
    checkout_el = checkin_checkout_el.format(month_year, day)
    
    while True:
        try:
            element = driver.find_elements_by_xpath(checkout_el)[1]
            element.click()
            break
        except Exception, e:
            further_element = driver.find_elements_by_xpath(further_el)[1]
            further_element.click() 

    ##### occupancy
    occupancy_element = './/select[@name="group_adults"]/option[contains(@value, "1")]'
    occupancy_element = process_elements.visibility(driver, occupancy_element, 10)
    occupancy_element.click()

    submit_element = '//button[@type="submit"]'
    submit_element = process_elements.visibility(driver, submit_element, 10)
    submit_element.click()
    
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    
    driver.quit()

def get_pages(driver, city, checkin, checkout, date):
    count = 0
    while True:
        scroll_down(driver)

        next_el = './/a[contains(@class, "paging-next")]'
        hotels = './/div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]'
        hotels = driver.find_elements_by_xpath(hotels)
        for hotel in hotels:
            count += 1
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'booking.com'
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
            
        time.sleep(20)
        try:
            next_element = process_elements.visibility(driver, next_el, 10)
            next_element.click()
        except:
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.booking.com/'
    scrape_dates()
    conn.close()


