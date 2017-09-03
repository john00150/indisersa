#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write, spider
import pyodbc, time
from datetime import datetime, timedelta

cities = [
    'Guatemala City, Guatemala',
#    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120]

def banner(element):
    try:
        banner = WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//div[@class="cookieControl"]/div/div/table/tbody/tr/td/a[@class="commit"]'))
        banner.click()
    except:
        pass

def scrape_name(element):
    return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//div[@class="innername"]/a').text.strip())

def scrape_address(element):
    return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[0].strip())

def scrape_location(element):
    return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[1].strip())

def scrape_price(element):
    try:
        new_price = WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@class="rateamount"]').text.strip().strip('Q').strip())
        old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//img[@class="rating_circles"]').get_attribute('title'))
    except:
        return 0

def scrape_review(element):
    return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//a[@class="ratingLink"]').text.strip())

def scrape_dates(url):
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date) 

def scrape_city(url, city, date):
    driver = spider(url)
    banner(driver)
    element_1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@name="city"]'))
    element_1.send_keys(city)
    element_2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@id="checkinDate"]'))
    element_2.click()
    time.sleep(5)

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)

    while True:
        try:
            driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day)).click()
            time.sleep(2)
            break
        except:
            driver.find_element_by_xpath('.//a[@data-handler="next"]').click()
            time.sleep(2)
        
    element_4 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@id="checkoutDate"]'))
    element_4.click()
    while True:
        try:
            driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)).click()
            time.sleep(2)
            break
        except:
            driver.find_element_by_xpath('.//a[@data-handler="next"]').click()
            time.sleep(2)
        
    element_6 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//a[contains(@title, "Search Destination")]'))
    element_6.click()
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    new_price, old_price = scrape_price(driver)
    name = scrape_name(driver)
    review = scrape_review(driver)
    rating = scrape_rating(driver)
    address = scrape_address(driver)
    city = city.split(',')[0]
    source = 'radisson.com'
    currency = 'GTQ'
    sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, 1, date)
    print '{}, checkin {}, checkout {}, range {}'.format(source, checkin, checkout, date)


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.radisson.com/'
    scrape_dates(url)
    conn.close()


