#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import spider, sql_connect, sql_write
import time, datetime

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

host = 'indisersa.database.windows.net'
username = 'otto'
password = 'Knoke@1958'
database = 'hotel_Info'


def banner(driver):
    try:
        driver.find_element_by_xpath('.//div/span[@class="title"][contains(text(), "Save an extra")]/following-sibling::span[@class="close-button"]').click()
    except:
        pass   

def scroll_down(driver):
    while True:
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath('.//div[@class="info unavailable-info"]')
            break
        except:
            pass

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
        for x in range(2):
            scrape_city(url, city, x, fh, conn, cur) 

def scrape_city(url, city, index, fh, conn, cur):
    driver = spider(url)
    element = driver.find_element_by_xpath('.//input[@name="q-destination"]')
    element.send_keys(city)
    element.click()
    banner(driver)
    time.sleep(2)

    if index == 0:
        checkin = datetime.date.today()
        checkin = checkin.strftime('%m/%d/%Y')

        delta = datetime.timedelta(days=2)
        checkout = datetime.date.today() + delta
        checkout_1 = checkout.strftime('%m/%d/%Y')
        checkout_2 = checkout.strftime('%m/%d/%y')

    if index == 1:
        delta_1 = datetime.timedelta(days=120)
        checkin = datetime.date.today() + delta_1
        checkin = checkin.strftime('%m/%d/%Y')

        delta_2 = datetime.timedelta(days=122)
        checkout = datetime.date.today() + delta_2
        checkout_1 = checkout.strftime('%m/%d/%Y')
        checkout_2 = checkout.strftime('%m/%d/%y')

    checkin_element = driver.find_element_by_xpath('//input[@name="q-localised-check-in"]')
    checkin_element.send_keys(checkin)
    banner(driver)
    time.sleep(2)
    checkout_element = driver.find_element_by_xpath('//input[@name="q-localised-check-out"]')
    checkout_element.clear()
    checkout_element.send_keys(checkout_2)
    banner(driver)
    try:
        driver.find_element_by_xpath('.//div[@class="widget-query-group widget-query-occupancy"]').click()
    except:
        pass
    time.sleep(2)

    occupancy_element = driver.find_element_by_xpath('.//select[@id="qf-0q-compact-occupancy"]/option[contains(text(), "1 room, 1 adult")]')
    occupancy_element.click()
    time.sleep(2)

    element = driver.find_element_by_xpath('//button[@type="submit"]')
    element.click()
    time.sleep(2)
    scrape_hotels(driver, city, checkin, checkout_1, fh, conn, cur)

    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, fh, conn, cur):
    count = 0
    scroll_down(driver)
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
    conn, cur = sql_connect(host, username, password, database)
    url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    fh = open('output/hotels.csv', 'w')
    header = 'name,review,rating,address,new_price,old_price,checkin,checkout,city\n'
    fh.write(header)
    scrape_cities(url, fh, conn, cur)
    fh.close()


