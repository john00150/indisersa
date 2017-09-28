#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write, spider
import pyodbc, time, sys
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [15, 30, 60, 90, 120]

currency = 'USD'
source = 'us.despegar.com'

def scroll_down(driver):
    element = driver.find_element_by_xpath('.//body')
    for x in range(150):
        element.send_keys(Keys.ARROW_DOWN)

def banner(driver):
    try:
        banner = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//i[@class="nevo-modal-close nevo-icon-close"]'))
        banner.click()
    except:
        try:
            banner = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//span[contains(@class, "eva-close")]'))
            banner.click()
        except:
            pass  

def scrape_name(element):
    WebDriverWait(element, 20).until(lambda element: element.find_element_by_xpath('.//h3[@class="hf-hotel-name"]/a'))
    return element.find_element_by_xpath('.//h3[@class="hf-hotel-name"]/a').get_attribute('title') 

def scrape_address(element):
    try:
        return element.find_element_by_xpath('.//li[@class="hf-cluster-distance"]/span').text.strip()
    except:
        return ''

def scrape_price(element):
    try:
        npr = element.find_element_by_xpath('.//li[@class="hf-pricebox-price"]').text.replace('USD', '').strip()
        new_price = '%s.%s' % (npr[:-2], npr[-2:])
        try:
            opr = element.find_element_by_xpath('.//span[contains(@class, "hf-pricebox-price-discount")]').text.replace('USD', '').strip()
            if len(opr) == 0:
                old_price = 0
            else:
                old_price = '%s.%s' % (opr[:-2], opr[-2:])
        except:
            old_price = 0
        return new_price, old_price
    except:
        return 0, 0

def scrape_rating(element):
    try:
        return element.find_element_by_xpath('.//span[contains(@class, "hf-raiting")]').text.strip()
    except:
        return 0

def scrape_review(element):
    return 0

def scrape_occupation(driver):
    try:
        element = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//select[contains(@class, "sbox-adults")]/option[@value="1"]'))
        element.click()
    except:
        element_1 = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//div[contains(@class, "sbox-guests-container")]'))
        element_1.click()
        element_2 = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//div[contains(@class, "stepper-adults")]/div/div/button[contains(@class, "button--dec")]'))
        element_2.click()
        element_3 = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//h3[contains(@class, "sbox-ui-heading")]'))
        element_3.click()

def scrape_dates():
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date) 

def scrape_city(url, city, date):
    driver = spider(url)
    driver.get(url)

    banner(driver)
    element_1 = './/input[contains(@class, "sbox-destination")]'
    element_1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, element_1)))
    element_1.send_keys(city)

    if city == 'Guatemala City, Guatemala':
        while True:
            try:
                driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Guatemala City, Guatemala, Guatemala")]')[1].click()
                time.sleep(2)
                break
            except:
                pass

    if city == 'Antigua Guatemala, Guatemala':
        while True:
            try:
                driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Antigua, Sacatepequez, Guatemala")]')[1].click()
                time.sleep(2)
                break
            except:
                pass

    element_2 = './/input[contains(@class, "sbox-checkin-date")]'
    element_2 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, element_2)))
    element_2.click()       

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)

    while True:
        try:
            element_4 = './/div[@data-month="{}"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "{}")]'.format(checkin.strftime('%Y-%m'), checkin.day)
            element_4 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, element_4)))
            element_4.click()
            break
        except:
            driver.find_element_by_xpath('.//div[contains(@class, "dpmg2--controls-next")]').click()
            time.sleep(2)

    while True:
        try:
            element_5 = './/div[@data-month="{}"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "{}")]'.format(checkout.strftime('%Y-%m'), checkout.day)
            element_5 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, element_5)))
            element_5.click()
            break
        except:
            driver.find_element_by_xpath('.//div[contains(@class, "dpmg2--controls-next")]').click()
            time.sleep(2)
    
    scrape_occupation(driver)
    element_6 = './/a[contains(@class, "sbox-search")]'
    element_6 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, element_6)))
    element_6.click()
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

def get_pages(driver, city, checkin, checkout, date):
    banner(driver)
    count = 0
    while True:
        hotels_1 = driver.find_elements_by_xpath('.//ul[@id="hotels"]/li[./div[@class="hf-cluster-card"]]')
        hotels_2 = driver.find_elements_by_xpath('.//div[contains(@class, "results-cluster-container")]')

        if len(hotels_1) == 0:
            hotels = hotels_2
        else:
            hotels = hotels_1        

        for hotel in hotels:
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            count += 1
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
        try:
            next = './/a[@data-ga-el="next"]'
            next = driver.find_element_by_xpath(next)
            next.click()
            banner(driver)
        except:
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.us.despegar.com/hotels/'
    scrape_dates()
    conn.close()


