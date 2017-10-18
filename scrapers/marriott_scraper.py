#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write
import pyodbc, time
from datetime import datetime, timedelta


dates = [15, 30, 60, 90, 120]

address = '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'
city = 'Guatemala City, Guatemala'
source = 'marriott.com'
currency = 'USD'
name = 'Courtyard Guatemala City'
rating = 0

def scrape_price(element):
    new_price = './/div[contains(@class, "t-price")]/span'
    new_price = element.find_element_by_xpath(new_price).text.strip()
    old_price = 0
    return new_price, old_price

def scrape_review(element):
    reviews_element = './/span[contains(text(), "Reviews")]'
    return element.find_element_by_xpath(reviews_element).text.strip()

def scrape_dates():
    for date in dates:
        scrape_hotel(url, date)

def scrape_hotel(url, date):
    driver = spider(url)
    time.sleep(5)

    review = scrape_review(driver)

    checkin = datetime.now() + timedelta(date)
    day = checkin.strftime('%A')[:3]
    month = checkin.strftime('%B')[:3]
    str1 = '{}, {} {}, {}'.format(day, month, checkin.day, checkin.year)
    checkout = datetime.now() + timedelta(date + 3)
    day2 = checkout.strftime('%A')[:3]
    month2 = checkout.strftime('%B')[:3]
    str2 = '{}, {} {}, {}'.format(day2, month2, checkout.day, checkout.year)

    input_elements = './/input[contains(@class, "js-date-from")]'
    input_elements = driver.find_elements_by_xpath(input_elements)

    print len(input_elements)
    if len(input_elements) == 10:
        input_elements = './/span[contains(@class, "l-close-icon")]'
    else:
        pass
        
    checkin_elms = './/div[@aria-label="{}"]'.format(str1)
    checkout_elms = './/div[@aria-label="{}"]'.format(str2)
    nextmonth_elms = './/div[@title="Next month"]'
    submit_elements = './/em[contains(text(), "View Rates")]'

    for x in input_elements:
        try:
            x.click()
            break
        except:
            pass

    time.sleep(5)

    done = False
    while True:   
        checkin_elements = driver.find_elements_by_xpath(checkin_elms)
        nextmonth_elements = driver.find_elements_by_xpath(nextmonth_elms)
        for x in checkin_elements:
            try:
                x.click()
                done = True
                break
            except Exception, e:
                pass

        if done == True:
            break

        for y in nextmonth_elements:
            try:
                y.click()
                break
            except Exception, e:
                pass

        time.sleep(5)

    done = False
    while True:
        checkout_elements = driver.find_elements_by_xpath(checkout_elms)
        nextmonth_elements = driver.find_elements_by_xpath(nextmonth_elms) 
  
        for x in checkout_elements:
            try:
                x.click()
                done = True
                break
            except:
                pass

        if done == True:
            break

        for y in nextmonth_elements:
            try:
                y.click()
                break
            except:
                pass

        time.sleep(2)

    review = scrape_review(driver)

    submit_elements = driver.find_elements_by_xpath(submit_elements)                                              
    for x in submit_elements:
        try:
            x.click()
            break
        except:
            pass

    time.sleep(10)

    scrape_rooms(driver, checkin, checkout, review, date)

    driver.quit()

def scrape_rooms(driver, checkin, checkout, review, date):
    checkin = checkin.strftime('%m/%d/%Y')
    checkout = checkout.strftime('%m/%d/%Y')
    rooms = driver.find_elements_by_xpath('.//div[contains(@class, "results-container")]/div[contains(@class, "m-room-rate-results")]')
    try:
        room = rooms[0]
        new_price, old_price = scrape_price(room)
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, 1, date)
        print '{}, checkin {}, checkout {}, range {}'.format(source, checkin, checkout, date)
    except Exception, e:
        print e

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
    scrape_dates()
    conn.close()


