#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write
import pyodbc, time
from datetime import datetime, timedelta


dates = [15, 30, 60, 90, 120]

def scrape_price(element):
    new_price = WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//div[contains(@class, "t-price")]/span').text.strip())
    old_price = 0
    return new_price, old_price

def scrape_review(element):
    return element.find_element_by_xpath('.//span[contains(text(), "Reviews")]').text.strip()

def scrape_dates():
    for date in dates:
        scrape_hotel(url, date)

def scrape_hotel(url, date):
    driver = spider(url)

    review = scrape_review(driver)

    checkin = datetime.now() + timedelta(date)
    day = checkin.strftime('%A')[:3]
    month = checkin.strftime('%B')[:3]
    str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)
    checkout = datetime.now() + timedelta(date + 3)
    day2 = checkout.strftime('%A')[:3]
    month2 = checkout.strftime('%B')[:3]
    str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    checkin_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@id="hws-fromDate"]'))
    checkin_element.click()
    time.sleep(2)

    done = False
    while not done:    
        for x in driver.find_elements_by_xpath('.//div[@aria-label="%s"]' % str1):
            try:
                x.click()
                time.sleep(5)
                done = True
            except:
                pass

        if done == True:
            break

        for y in driver.find_elements_by_xpath('.//div[@title="Next month"]'):
            try:
                y.click()
                time.sleep(2)
            except:
                pass

    done = False
    while not done:    
        for x in driver.find_elements_by_xpath('.//div[@aria-label="%s"]' % str2):
            try:
                x.click()
                time.sleep(5)
                done = True
            except:
                pass

        if done == True:
            break

        for y in driver.find_elements_by_xpath('.//div[@title="Next month"]'):
            try:
                y.click()
                time.sleep(2)
            except:
                pass

    review = scrape_review(driver)
                                                            
    driver.find_elements_by_xpath('.//button[contains(text(), "VIEW RATES")]')[0].click()
    time.sleep(5)
    scrape_rooms(driver, checkin, checkout, review, date)
    driver.quit()

def scrape_rooms(driver, checkin, checkout, review, date):
    checkin = checkin.strftime('%m/%d/%Y')
    checkout = checkout.strftime('%m/%d/%Y')
    rooms = driver.find_elements_by_xpath('.//div[contains(@class, "results-container")]/div[contains(@class, "m-room-rate-results")]')
    for room in rooms[:1]:
        new_price, old_price = scrape_price(room)
        name = 'Courtyard Guatemala City'
        rating = 0
        address = '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'
        city = 'Guatemala City, Guatemala'
        source = 'marriott.com'
        currency = 'USD'
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, 1, date)
        print '{}, checkin {}, checkout {}, range {}'.format(source, checkin, checkout, date)

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


