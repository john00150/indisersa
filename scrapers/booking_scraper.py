#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_write
import time, pyodbc
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def banner(driver):
    try:
        driver.find_element_by_xpath('.//body').click()
    except:
        pass 

def spider(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    return driver 

def scroll_down(driver):
    for x in range(500):
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.4)

def scrape_name(element):
    name = element.find_element_by_xpath('.//span[@class="sr-hotel__name"]').text 
    return name

def scrape_address(element):
    return element.find_element_by_xpath('.//div[@class="address"]/a').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/strong/b').text.strip().strip('GTQ').strip().replace(',', '')
        try:
            old_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span').text.strip().strip('GTQ').strip().replace(',', '')
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//span[@itemprop="ratingValue"]').text.strip()
    except:
        return 0

def scrape_review(element):
    try:
        review = element.find_element_by_xpath('.//span[@class="score_from_number_of_reviews"]').text
        return review
    except:
        return 0

def scrape_cities(url):
    for city in cities[:]:
        for x in range(2):
            scrape_city(url, city, x) 

def scrape_city(url, city, index):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[@id="ss"][@class="c-autocomplete__input sb-searchbox__input sb-destination__input"]').send_keys(city)
    time.sleep(2)
    if city == 'Guatemala City, Guatemala':
        driver.find_element_by_xpath('.//b[@class="search_hl_name"][contains(text(), "Guatemala (Guatemala City)")]').click()
        time.sleep(2)
    if city == 'Antigua Guatemala, Guatemala':
        driver.find_element_by_xpath('.//b[@class="search_hl_name"][contains(text(), "Antigua Guatemala")]').click()
        time.sleep(2)

    if index == 0:
        checkin = datetime.now()
        str1 = '%s %s' % (checkin.strftime('%B'), checkin.year)
        driver.find_elements_by_xpath('.//div[@data-mode="checkin"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str1, checkin.day))[0].click()
        time.sleep(2)

        checkout = datetime.now() + timedelta(days=2)
        str2 = '%s %s' % (checkout.strftime('%B'), checkin.year)
        driver.find_elements_by_xpath('.//div[@data-placeholder="Check-out Date"]')[0].click()
        time.sleep(2)
        driver.find_elements_by_xpath('.//div[@data-mode="checkout"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str2, checkout.day))[0].click()
        time.sleep(2)

    if index == 1:
        def get_month():
            for x in range(4):      
                driver.find_elements_by_xpath('.//div[@class="c2-calendar-body"]/div/span[@class="c2-button-inner"]')[1].click()
                time.sleep(1)

        delta1 = timedelta(days=120)
        checkin = datetime.now() + delta1
        str1 = '%s %s' % (checkin.strftime('%B'), checkin.year)
        get_month()
        driver.find_elements_by_xpath('.//div[@data-mode="checkin"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str1, checkin.day))[0].click()
        time.sleep(2)

        delta2 = timedelta(days=122)
        checkout = datetime.now() + delta2
        str2 = '%s %s' % (checkout.strftime('%B'), checkout.year)
        driver.find_elements_by_xpath('.//div[@data-placeholder="Check-out Date"]')[0].click()
        time.sleep(2)
        driver.find_elements_by_xpath('.//div[@data-mode="checkout"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str2, checkout.day))[0].click()
        time.sleep(2)

    driver.find_element_by_xpath('.//select[@name="group_adults"]/option[contains(@value, "1")]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(5)
    get_pages(driver, city, checkin, checkout)

    driver.quit()

def get_pages(driver, city, checkin, checkout):
    checkin = checkin.date()
    checkout = checkout.date()
    count = 0
    while True:
        scroll_down(driver)
        hotels = driver.find_elements_by_xpath('.//div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]')
        for hotel in hotels:
            new_price, old_price = scrape_price(hotel)
            name = scrape_name(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'booking.com'
            location = scrape_address(hotel)
            count += 1
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, location)
         
        try:
            driver.find_element_by_xpath('.//a[contains(@class, "paging-next")]').click()
            time.sleep(10)
        except:
            driver.quit()
            print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.booking.com/'
    scrape_cities(url)
    conn.close()


