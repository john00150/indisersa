#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write
import pyodbc, time, os
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120]

def banner(driver):
    try:
        driver.find_element_by_xpath('.//body').click()
    except:
        pass 

def spider(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver 

def scroll_down(driver):
    time.sleep(5)
    elements = driver.find_elements_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/strong[contains(@class, "price scarcity_color")]/b')
    while True:
        driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.4)
        elements_2 = [e for e in elements if len(e.text.strip())!=0]
        if len(elements) == len(elements_2):
            break

def scrape_name(element):
    return element.find_element_by_xpath('.//span[contains(@class, "sr-hotel__name")]').text 

def scrape_address(element):
    return element.find_element_by_xpath('.//div[@class="address"]/a').text.strip()

def scrape_price(element):
    try:
        new_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/strong/b').text.strip().strip('GTQ').strip().replace(',', '')
        try:
            old_price = element.find_element_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span').text.strip().strip('GTQ').strip().replace(',', '')
        except:
            old_price = 0
        return int(new_price)/3, int(old_price)/3
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

def scrape_dates():
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date)

def scrape_city(url, city, date):
    driver = spider(url)
    element_1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@id="ss"][@class="c-autocomplete__input sb-searchbox__input sb-destination__input"]'))
    element_1.send_keys(city)
    time.sleep(5)
    if city == 'Guatemala City, Guatemala':
        driver.find_element_by_xpath('.//li[contains(@data-label, "Guatemala, Guatemala, Guatemala")]').click()

    if city == 'Antigua Guatemala, Guatemala':
        driver.find_element_by_xpath('.//li[contains(@data-label, "Antigua Guatemala, Guatemala")]').click()

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)
    str1 = '%s %s' % (checkin.strftime('%B'), checkin.year)
    str2 = '%s %s' % (checkout.strftime('%B'), checkout.year)
    time.sleep(5)

    while True:
        try:
            driver.find_element_by_xpath('.//div[@data-mode="checkin"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str1, checkin.day)).click()
            break
        except Exception, e:
            #ee = driver.find_elements_by_xpath('.//div[contains(@class, "c2-button-further")]/span[contains(@class, "c2-button-inner")]')
            ee = driver.find_elements_by_xpath('.//div[contains(@class, "c2-button-further")]')
            for e in ee:
                try:
                    e.click()
                    time.sleep(2)
                    break
                except:
                    pass

    driver.find_element_by_xpath('.//div[@data-placeholder="Check-out Date"]').click()
    time.sleep(5)

    while True:
        try:
            driver.find_element_by_xpath('.//div[@data-mode="checkout"]/following-sibling::div/div[@class="c2-calendar-body"]/div/div/div[@class="c2-months-table"]/div[@class="c2-month"]/table[@class="c2-month-table"][./thead/tr[@class="c2-month-header"]/th[contains(text(), "%s")]]/tbody/tr/td/span[contains(text(), "%s")]' % (str2, checkout.day)).click()
            break
        except:
            ee = driver.find_elements_by_xpath('.//div[contains(@class, "c2-button-further")]')
            for e in ee:
                try:
                    e.click()
                    time.sleep(2)
                    break
                except:
                    pass

    driver.find_element_by_xpath('.//select[@name="group_adults"]/option[contains(@value, "1")]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(2)
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    driver.quit()

def get_pages(driver, city, checkin, checkout, date):
    count = 0
    while True:
        scroll_down(driver)
        #time.sleep(10)
        hotels = driver.find_elements_by_xpath('.//div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]')
        for hotel in hotels:
            count += 1
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'GTQ'
            source = 'booking.com'
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
            
        time.sleep(15)
        try:
            driver.find_element_by_xpath('.//a[contains(@class, "paging-next")]').click()
        except:
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.booking.com/'
    scrape_dates()
    conn.close()


