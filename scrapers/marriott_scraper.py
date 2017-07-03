#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_connect, sql_write
import time, datetime

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

host = 'indisersa.database.windows.net'
username = 'otto'
password = 'Knoke@1958'
database = 'hotel_Info'


def scroll_down(driver):
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath('.//span[contains(text(), "See more options")]').click()
            time.sleep(5)
        except:
            break

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
    driver.find_elements_by_xpath('.//input[@name="destinationAddress.destination"]')[1].send_keys(city)
    time.sleep(2)

    if index == 0:
        checkin = datetime.datetime.now()
        day = checkin.strftime('%A')[:3]
        month = checkin.strftime('%B')[:3]
        str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)

        delta = datetime.timedelta(days=2)
        checkout = datetime.datetime.now() + delta
        day2 = checkout.strftime('%A')[:3]
        month2 = checkout.strftime('%B')[:3]
        str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    if index == 1:
        delta_1 = datetime.timedelta(days=120)
        checkin = datetime.datetime.now() + delta_1
        day = checkin.strftime('%A')[:3]
        month = checkin.strftime('%B')[:3]
        str1 = '%s, %s %s, %s' % (day, month, checkin.day, checkin.year)

        delta_2 = datetime.timedelta(days=122)
        checkout = datetime.datetime.now() + delta_2
        day2 = checkout.strftime('%A')[:3]
        month2 = checkout.strftime('%B')[:3]
        str2 = '%s, %s %s, %s' % (day2, month2, checkout.day, checkout.year)

    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].click()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].clear()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].send_keys(str1)
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-out"]')[1].clear()
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-out"]')[1].send_keys(str2)
    time.sleep(2)
    driver.find_elements_by_xpath('.//input[@placeholder="Check-in"]')[1].click()
    time.sleep(2)
    driver.find_elements_by_xpath('.//button[@title="Find"]')[1].click() # submit
    time.sleep(5)
    #scrape_hotels(driver)#, city, checkin, checkout_1, fh, conn, cur)
    driver.quit()

def scrape_hotels(driver):#, city, checkin, checkout, fh, conn, cur):
    time.sleep(5)
    count = 0
    scroll_down(driver)
    hotels = driver.find_elements_by_xpath('.//ul[@id="hotelList"]/li[contains(@class, "hotel-item")]')
    print len(hotels)
    #for hotel in hotels:
    #    new_price, old_price = scrape_price(hotel)
    #    name = hotel.get_attribute('data-title')
    #    review = scrape_review(hotel)
    #    rating = scrape_rating(hotel)
    #    address = scrape_address(hotel)
    #    new_price = new_price
    #    old_price = old_price
    #    checkin = checkin
    #    checkout = checkout
    #    city = city.split(',')[0]     
    #    if city not in address:
    #        continue
    #    count += 1

    #    line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, review, rating, address, new_price, old_price, checkin, checkout, city)
    #    fh.write(line.encode('utf8'))
    #    sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city)

    #print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)

def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)
    return driver


if __name__ == '__main__':
    conn = None
    cur = None
    #conn, cur = sql_connect(host, username, password, database)
    url = 'http://www.marriott.com/search/default.mi'
    fh = open('output/marriott.csv', 'w')
    header = 'name,review,rating,address,new_price,old_price,checkin,checkout,city\n'
    fh.write(header)
    scrape_cities(url, fh, conn, cur)
    fh.close()


