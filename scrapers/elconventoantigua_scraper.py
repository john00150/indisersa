#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_write, spider
import time, pyodbc
from datetime import datetime, timedelta


def scrape_name():
    return 'Convento Boutique Hotel'

def scrape_address():
    return '2a Avenida Norte #11, Antigua Guatemala +502 7720 7272'

def scrape_location():
    return 'Antigua Guatemala'

def scrape_price(element):
    new_price = element.find_elements_by_xpath('.//div[contains(@class, "CardList-price-title")]')[0].text.strip().strip('$').strip()
    old_price = 0
    return new_price, old_price

def scrape_rating():
    return 0

def scrape_review():
    return 0

def scrape_dates(url):
    for x in range(2):
        scrape(url, x) 

def scrape(url, index):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[@id="date-in"]').click()
    time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        checkout = datetime.now() + timedelta(days=2)

    if index == 1:
        checkin = datetime.now() + timedelta(days=120)
        checkout = datetime.now() + timedelta(days=122)
        for x in range(4):
            driver.find_element_by_xpath('.//a[@title="Next"]').click()
            time.sleep(1)

    driver.find_element_by_xpath('.//table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//select[@id="adults"]/option[contains(text(), "1")]').click()
    time.sleep(2)
    driver.find_element_by_xpath('.//select[@id="rooms"]/option[contains(text(), "1")]').click()
    time.sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    driver.find_element_by_xpath('.//button[@type="submit"]').click()
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[1])
    scrape_hotels(driver, checkin, checkout)
    driver.quit()

def scrape_hotels(driver, checkin, checkout):
    time.sleep(10)
    new_price, old_price = scrape_price(driver)
    name = scrape_name()
    review = scrape_review()
    rating = scrape_rating()
    address = scrape_address()
    city = 'Antigua Guatemala, Guatemala'
    location = scrape_location()     
    source = 'elconventoantigua.com'
    currency = 'USD'
    #sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin.date(), checkout.date(), city, currency, source, location)


if __name__ == '__main__':
    global conn
    global cur
    #conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    #cur = conn.cursor()
    url = 'http://www.elconventoantigua.com/suites-convento-boutique-hotel-,rooms-en.html'
    scrape_dates(url)
    #conn.close()


