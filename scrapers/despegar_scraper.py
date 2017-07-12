#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from processors import sql_write, spider
import time, pyodbc
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

def banner(driver):
    try:
        driver.find_element_by_xpath('.//i[@class="nevo-modal-close nevo-icon-close"]').click()
        time.sleep(2)
    except:
        pass 

def scrape_name(element):
    name = element.find_element_by_xpath('.//h3[@class="hf-hotel-name"]/a').get_attribute('title') 
    return name

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
        driver.find_element_by_xpath('.//select[contains(@class, "sbox-adults")]/option[@value="1"]').click()
        time.sleep(2)
    except:
        driver.find_element_by_xpath('.//div[contains(@class, "sbox-guests-container")]').click()
        time.sleep(2)
        driver.find_element_by_xpath('.//div[contains(@class, "stepper-adults")]/div/div/button[contains(@class, "button--dec")]').click()
        time.sleep(2)
        driver.find_element_by_xpath('.//h3[contains(@class, "sbox-ui-heading")]').click()
        time.sleep(2)

def send_city_name(url, city):
    driver = spider(url)
    driver.find_element_by_xpath('.//input[contains(@class, "sbox-destination")]').send_keys(city)
    time.sleep(5)

    if city == 'Guatemala City, Guatemala':
        driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Guatemala City, Guatemala, Guatemala")]')[1].click()
        time.sleep(2)
    if city == 'Antigua Guatemala, Guatemala':
        driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Antigua, Sacatepequez, Guatemala")]')[1].click()
        time.sleep(2)
    return driver

def scrape_cities(url):
    for city in cities:
        scrape_city(url, city) 

def scrape_city(url, city):
    try:
        driver = send_city_name(url, city)
    except:
        driver.quit()
        driver = send_city_name(url, city)
    driver.find_element_by_xpath('.//input[contains(@class, "sbox-checkin-date")]').click()       

    checkin = datetime.now() + timedelta(days=15)
    checkout = datetime.now() + timedelta(days=18)
    driver.find_element_by_xpath('.//div[@data-month="%s"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "%s")]' % (checkin.strftime('%Y-%m'), checkin.day)).click()
    time.sleep(2)
    driver.find_element_by_xpath('.//div[@data-month="%s"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "%s")]' % (checkout.strftime('%Y-%m'), checkout.day)).click()
    time.sleep(2)    

    scrape_occupation(driver)
    driver.find_element_by_xpath('.//a[contains(@class, "sbox-search")]').click()
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'))

def get_pages(driver, city, checkin, checkout):
    time.sleep(10)
    banner(driver)
    count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        hotels = driver.find_elements_by_xpath('.//ul[@id="hotels"]/li[./div[@class="hf-cluster-card"]]')
        for hotel in hotels:
            new_price, old_price = scrape_price(hotel)
            name = scrape_name(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'USD'
            source = 'us.despegar.com'
            #location = scrape_address(hotel)
            count += 1
            sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
        try:
            driver.find_element_by_xpath('.//div[@class="pagination"]/ul/li[contains(@class, "next")]').click()
            time.sleep(5)
            banner(driver)
            time.sleep(5)
        except:
            driver.quit()
            print '%s, %s hotels, checkin %s, checkout %s' % (city, count, checkin, checkout)
            break


if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'https://www.us.despegar.com/hotels/'
    scrape_cities(url)
    conn.close()


