#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import spider, sql_write
import pyodbc, time
from datetime import datetime, timedelta

cities = [
    'Antigua Guatemala, Guatemala',   
    'Guatemala City, Guatemala',
]


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

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city)  

def scrape_city(url, city):
    driver = spider(url)
    element = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//div[@class="hcsb_citySearchWrapper"]/input'))
    element.send_keys(city)
    element_2 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//ul[@id="ui-id-1"]/li'))
    element_2.click()

    checkin = datetime.now() + timedelta(days=15)
    checkin_year_month = '%s-%s' % (checkin.year, checkin.month)
    checkout = datetime.now() + timedelta(days=18)
    checkout_year_month = '%s-%s' % (checkout.year, checkout.month)

    element_3 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('//select[@class="hcsb_checkinDay"]/option[@value="%s"]' % checkin.day))
    element_3.click()
    element_4 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('//select[@class="hcsb_checkinMonth"]/option[@value="%s"]' % checkin_year_month))
    element_4.click()
    element_5 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('//select[@class="hcsb_checkoutDay"]/option[@value="%s"]' % checkout.day))
    element_5.click()
    element_6 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('//select[@class="hcsb_checkoutMonth"]/option[@value="%s"]' % checkout_year_month))
    element_6.click()
    element_7 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//button[contains(@class, "ui-datepicker-close")]'))
    element_7.click()
    element_8 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('.//select[@class="hcsb_guests"]/option[@value="1-1"]'))
    element_8.click()
    element_9 = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath('//a[@class="hcsb_searchButton"]'))
    element_9.click()
    WebDriverWait(driver, 20).until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to_window(driver.window_handles[1])
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))
    driver.quit()

def scrape_hotels(driver, city, count, checkin, checkout):
    while True:
        WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_xpath('.//div[@class="hc_sr_summary"]/div[@class="hc_sri hc_m_v4"]')) > 0)
        hotels = driver.find_elements_by_xpath('.//div[@class="hc_sr_summary"]/div[@class="hc_sri hc_m_v4"]')
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
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count)
        time.sleep(10)
        try:
            _next = WebDriverWait(driver, 10).until(driver.find_element_by_xpath('.//a[@data-paging="next"]'))
            _next.click()
        except:
            print '%s, %s, %s hotels, checkin %s, checkout %s' % (source, city, count, checkin, checkout)
            break

def get_pages(driver, city, checkin, checkout):
    count = 0
    while True:
        try:
            scrape_hotels(driver, city, count, checkin, checkout)
            break
        except:
            pass

if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'http://www.book-hotel-beds.com/'
    scrape_cities(url)
    conn.close()


