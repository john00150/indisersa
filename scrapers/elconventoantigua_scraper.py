#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from processors import sql_write
import time, pyodbc
from datetime import datetime, timedelta


def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(800, 1200)
    driver.get(url)
    return driver

def scrape_name():
    return 'Convento Boutique Hotel'

def scrape_address():
    return '2a Avenida Norte #11, Antigua Guatemala +502 7720 7272'

def scrape_location():
    return 'Antigua Guatemala'

def scrape_price(element):
    new_price = WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//div[contains(@class, "CardList-price-title")]').text.strip().strip('$').strip())
    old_price = 0
    return new_price, old_price

def scrape_rating():
    return 0

def scrape_review():
    return 0

def scrape_dates(url):
    scrape(url) 

def scrape(url):
    driver = spider(url)
    element_1 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//input[@id="date-in"]'))
    element_1.click()

    checkin = datetime.now() + timedelta(days=15)
    checkout = datetime.now() + timedelta(days=18)

    try:
        element_2 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, './/table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day))))
        element_2.click()
    except:
        driver.find_element_by_xpath('.//a[contains(@class, "ui-datepicker-next")]').click()
        element_2 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, './/table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day))))
        element_2.click()
    try:
        element_3 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)))
        element_3.click()
    except:
        driver.find_element_by_xpath('.//a[contains(@class, "ui-datepicker-next")]').click()
        element_3 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)))
        element_3.click()   
    element_4 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//select[@id="adults"]/option[contains(text(), "1")]'))
    element_4.click()
    element_5 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//select[@id="rooms"]/option[contains(text(), "1")]'))
    element_5.click()
    element_6 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//button[@type="submit"]'))
    element_6.click()
    WebDriverWait(driver, 20).until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to_window(driver.window_handles[1])
    scrape_hotels(driver, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))
    driver.quit()

def scrape_hotels(driver, checkin, checkout):
    try:
        new_price, old_price = scrape_price(driver)
        name = scrape_name()
        review = scrape_review()
        rating = scrape_rating()
        address = scrape_address()
        city = 'Antigua Guatemala, Guatemala'
        source = 'elconventoantigua.com'
        currency = 'USD'
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
        print name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source 
    except:
        print 'the date is unavailable'


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'http://www.elconventoantigua.com/suites-convento-boutique-hotel-,rooms-en.html'
    scrape_dates(url)
    conn.close()


