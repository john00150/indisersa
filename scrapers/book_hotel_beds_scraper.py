#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import spider, sql_connect, sql_write
import time, datetime

cities = [
    'Guatemala City, Guatemala',
#    'Antigua Guatemala, Guatemala',
]

host = 'indisersa.database.windows.net'
username = 'otto'
password = 'Knoke@1958'
database = 'hotel_Info'


def scrape_address(driver):
    elements = driver.find_elements_by_xpath('.//div[@class="contact"]/p')
    line = ''
    elements_1 = ' '.join([x.text for x in elements[0].find_elements_by_xpath('./span')])
    elements_2 = elements[1].text
    line = '%s, %s.' % (elements_1, elements_2)
    return line

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//span[@class="old-price-cont"]/ins').text
        old_price = element.find_element_by_xpath('.//span[@class="old-price-cont"]/del').text
        return new_price, old_price
    except:
        try:
            new_price = element.find_element_by_xpath('.//b[@class="fewRoomsLeft"]').text
            old_price = None #element.find_element_by_xpath('.//')
            return new_price, old_price
        except:
            new_price = None
            old_price = element.find_element_by_xpath('.//div[@class="price"]/a/b').text
            return new_price, old_price

def scrape_rating(element):
    try:
        rating = element.find_element_by_xpath('.//div[contains(@class, "guest-rating")]').text.strip()
        return rating
    except:
        return None

def scrape_review(element):
    try:
        review = element.find_element_by_xpath('.//div[@class="guest-reviews-link"]/a/span[@class="full-view"]').text
        return review
    except:
        return None

def scrape_cities(url, fh, conn, cur):
    for city in cities:
        for x in range(1):
            scrape_city(url, city, x, fh, conn, cur) 

def scrape_city(url, city, index, fh, conn, cur):
    driver = spider(url)
    element = driver.find_elements_by_xpath('.//div[@class="hcsb_citySearchWrapper"]/input')[0]
    element.send_keys(city)
    time.sleep(2)
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
    get_pages(driver, fh)
    driver.quit()

def get_pages(driver, fh):
    time.sleep(5)
    #scrape_hotels(driver, city, checkin, checkout_1, fh, conn, cur)
    while True:
        try:
            driver.find_element_by_xpath('.//a[@data-paging="next"]').click()
            time.sleep(5)
        except:
            break

def scrape_hotels(driver, city, checkin, checkout, fh, conn, cur):
    count = 0
    hotels = driver.find_elements_by_xpath('.//ol[contains(@class, "listings")]/li[contains(@class, "hotel")]')
    for hotel in hotels:
        new_price, old_price = scrape_price(hotel)
        name = hotel.get_attribute('data-title')
        review = scrape_review(hotel)
        rating = scrape_rating(hotel)
        address = scrape_address(hotel)
        new_price = new_price
        old_price = old_price
        checkin = checkin
        checkout = checkout
        city = city.split(',')[0]     
        if city not in address:
            continue
        count += 1

        line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, review, rating, address, new_price, old_price, checkin, checkout, city)
        fh.write(line.encode('utf8'))
        sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city)

    print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)


if __name__ == '__main__':
    #conn, cur = sql_connect(host, username, password, database)
    conn = None
    cur = None
    url = 'http://www.book-hotel-beds.com/'
    fh = open('output/book_hotel_beds.csv', 'w')
    header = 'name,review,rating,address,new_price,old_price,checkin,checkout,city\n'
    fh.write(header)
    scrape_cities(url, fh, conn, cur)
    fh.close()


