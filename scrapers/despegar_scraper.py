#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write
import pyodbc, time, sys
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

banners = [
    './/i[@class="nevo-modal-close nevo-icon-close"]',
    './/span[contains(@class, "eva-close")]',
]

dates = [15, 30, 60, 90, 120]

url = 'https://www.us.despegar.com/hotels/'
currency = 'USD'
source = 'us.despegar.com'

def spider():
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def scroll_down(driver):
    element = driver.find_element_by_xpath('.//body')
    for x in range(150):
        element.send_keys(Keys.ARROW_DOWN)

def banner(driver):
    for banner in banners:
        try:
            banner_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, banner)))
            banner_element.click()
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
        rating = './/span[contains(@class, "hf-raiting")]'
        rating = element.find_element_by_xpath(rating).text.strip()
        return rating
    except:
        return 0

def scrape_review(element):
    return 0

def scrape_occupation(driver):
    try:
        occupation_element1 = './/select[contains(@class, "sbox-adults")]/option[@value="1"]' 
        occupation_element1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, occupation_element1)))
        occupation_element1.click()
    except:
        occupation_element1 = './/div[contains(@class, "sbox-guests-container")]'
        occupation_element1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, occupation_element1)))
        occupation_element1.click()
        occupation_element2 = './/div[contains(@class, "stepper-adults")]/div/div/button[contains(@class, "button--dec")]'
        occupation_element2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, occupation_element2)))
        occupation_element2.click()
        occupation_element3 = './/div[contains(@class, "full")]'
        occupation_element3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, occupation_element3)))
        occupation_element3.click()

def scrape_dates():
    for date in dates:
        scrape_cities(url, date)

def scrape_cities(url, date):
    for city in cities:
        scrape_city(url, city, date) 

def scrape_city(url, city, date):
    driver = spider()

    banner(driver)
    
    city_element = './/input[contains(@class, "sbox-destination")]'
    city_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, city_element)))
    city_element.send_keys(city)

    if city == 'Guatemala City, Guatemala':
        city_el2 = './/*[contains(., "Guatemala City, Guatemala, Guatemala")]'

    if city == 'Antigua Guatemala, Guatemala':
        city_el2 = './/*[contains(., "Antigua, Sacatepequez, Guatemala")]'

    city_el = './/div[@class="geo-searchbox-autocomplete-holder-transition"]'

        
    while True:
        try:
            city_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, city_el)))
            city_element = city_element.find_elements_by_xpath(city_el2)[1]
            city_element.click()
            break
        except:
            pass

    checkin_click_element = './/input[contains(@class, "sbox-checkin-date")]'
    checkin_click_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, checkin_click_element)))
    checkin_click_element.click()       

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)

    checkin_el = './/div[@data-month="{}"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "{}")]'\
                 .format(checkin.strftime('%Y-%m'), checkin.day)
    checkout_el = './/div[@data-month="{}"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "{}")]'\
                 .format(checkout.strftime('%Y-%m'), checkout.day)
    next_el = './/div[contains(@class, "dpmg2--controls-next")]'

    while True:
        try:
            checkin_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, checkin_el)))
            checkin_element.click()
            break
        except:
            next_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, next_el)))
            next_element.click()
            time.sleep(5)

    while True:
        try:
            checkout_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, checkout_el)))
            checkout_element.click()
            break
        except:
            next_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, next_el)))
            next_element.click()
            time.sleep(5)
    
    scrape_occupation(driver)
    
    submit_element = './/a[contains(@class, "sbox-search")]'
    submit_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, submit_element)))
    submit_element.click()
    
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

def get_pages(driver, city, checkin, checkout, date):
    next_el = './/a[@data-ga-el="next"]'

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
            next_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, next_el)))
            next_element.click()
            
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
    scrape_dates()
    conn.close()


