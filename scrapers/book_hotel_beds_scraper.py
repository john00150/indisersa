#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import spider, sql_write
import time, datetime, pyodbc

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]


def scrape_address(element):
    try:
        return element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_location")]').text
    except:
        return ''

def scrape_name(element):
    return element.find_element_by_xpath('.//a[contains(@data-ceid, "searchresult_hotelname")]').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_price")]').text.strip().split(' ')[1].replace(',', '')
        try:
            old_price = element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_wasPrice")]').text.strip().split(' ')[1].replace(',', '')
        except:
            old_price = ''
        return new_price, old_price
    except:
        return '', ''

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//p[@class="hc_hotel_userRating"]/a').text.strip()
    except:
        return ''

def scrape_review(element):
    try:
        return element.find_element_by_xpath('.//p[contains(@class, "hc_hotel_numberOfReviews")]/span').text.strip()
    except:
        return ''

def scrape_cities(url):
    for city in cities:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    element = driver.find_elements_by_xpath('.//div[@class="hcsb_citySearchWrapper"]/input')[0]
    element.send_keys(city)
    time.sleep(5)
    driver.find_element_by_xpath('.//ul[@id="ui-id-1"]/li').click()
    time.sleep(2)
    driver.find_element_by_xpath('//select[@class="hcsb_checkinDay"]').click()
    time.sleep(2)

    if index == 0:
        checkin = datetime.datetime.now()
        checkin_year_month = '%s-%s' % (checkin.year, checkin.month)

        delta = datetime.timedelta(days=2)
        checkout = datetime.datetime.now() + delta
        checkout_year_month = '%s-%s' % (checkout.year, checkout.month)

    if index == 1:
        delta_1 = datetime.timedelta(days=120)
        checkin = datetime.datetime.now() + delta_1
        checkin_year_month = '%s-%s' % (checkin.year, checkin.month)

        delta_2 = datetime.timedelta(days=122)
        checkout = datetime.datetime.now() + delta_2
        checkout_year_month = '%s-%s' % (checkout.year, checkout.month)

    driver.find_element_by_xpath('//select[@class="hcsb_checkinDay"]/option[@value="%s"]' % checkin.day).click()
    time.sleep(2)
    driver.find_element_by_xpath('//select[@class="hcsb_checkinMonth"]/option[@value="%s"]' % checkin_year_month).click()
    time.sleep(2)
    driver.find_element_by_xpath('//select[@class="hcsb_checkoutDay"]/option[@value="%s"]' % checkout.day).click()
    time.sleep(2)
    driver.find_element_by_xpath('//select[@class="hcsb_checkoutMonth"]/option[@value="%s"]' % checkout_year_month).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//select[@class="hcsb_guests"]/option[@value="1-1"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//a[@class="hcsb_searchButton"]').click()
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[1])
    get_pages(driver, city, checkin, checkout)
    driver.quit()

def get_pages(driver, city, checkin, checkout):
    checkin = checkin.date()
    checkout = checkout.date()
    time.sleep(5)
    count = 0
    while True:
        hotels = driver.find_elements_by_xpath('.//div[@class="hc_sr_summary"]/div[@class="hc_sri hc_m_v4"]')
        for hotel in hotels:
            new_price, old_price = scrape_price(hotel)
            name = scrape_name(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = scrape_address(hotel)
            checkin = checkin
            checkout = checkout
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'book-hotel-beds.com'
            if len(new_price) == 0 and len(old_price) == 0:
                continue
            count += 1
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
        try:
            driver.find_element_by_xpath('.//a[@data-paging="next"]').click()
            time.sleep(10)
        except:
            print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    url = 'http://www.book-hotel-beds.com/'
    scrape_cities(url)
    conn.close()


