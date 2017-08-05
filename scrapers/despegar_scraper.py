#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from processors import sql_write#, spider
import pyodbc, time
from datetime import datetime, timedelta


cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

dates = [60, 15, 30, 60, 90, 120]


def spider(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=159.203.117.131:3128')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    return driver

def banner(driver):
    try:
        banner = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('.//i[@class="nevo-modal-close nevo-icon-close"]'))
        banner.click()
    except:
        pass
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
    element_1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[contains(@class, "sbox-destination")]'))
    element_1.send_keys(city)

    if city == 'Guatemala City, Guatemala':
        WebDriverWait(driver, 10).until(lambda driver: len(driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Guatemala City, Guatemala, Guatemala")]')) > 0)
        driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Guatemala City, Guatemala, Guatemala")]')[1].click()

    if city == 'Antigua Guatemala, Guatemala':
        WebDriverWait(driver, 10).until(lambda driver: len(driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Antigua, Sacatepequez, Guatemala")]')) > 0)
        driver.find_element_by_xpath('.//div[@class="geo-searchbox-autocomplete-holder-transition"]').find_elements_by_xpath('.//*[contains(., "Antigua, Sacatepequez, Guatemala")]')[1].click()

    element_2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[contains(@class, "sbox-checkin-date")]'))
    element_2.click()       

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)

    while True:
        try:
            element_4 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//div[@data-month="%s"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "%s")]' % (checkin.strftime('%Y-%m'), checkin.day)))
            element_4.click()
            break
        except:
            driver.find_element_by_xpath('.//div[@class="_dpmg2--controls-next"]').click()
            time.sleep(2)

    while True:
        try:
            element_5 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//div[@data-month="%s"]/div[contains(@class, "dpmg2--dates")]/span[contains(text(), "%s")]' % (checkout.strftime('%Y-%m'), checkout.day)))
            element_5.click()
            break
        except:
            driver.find_element_by_xpath('.//div[@class="_dpmg2--controls-next"]').click()
            time.sleep(2)
    
    scrape_occupation(driver)
    element_6 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//a[contains(@class, "sbox-search")]'))
    element_6.click()
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)

def get_pages(driver, city, checkin, checkout, date):
    banner(driver)
    count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(lambda driver: len(driver.find_elements_by_xpath('.//ul[@id="hotels"]/li[./div[@class="hf-cluster-card"]]')) > 0)
        hotels = driver.find_elements_by_xpath('.//ul[@id="hotels"]/li[./div[@class="hf-cluster-card"]]')
        for hotel in hotels:
            name = scrape_name(hotel)
            new_price, old_price = scrape_price(hotel)
            review = scrape_review(hotel)
            rating = scrape_rating(hotel)
            address = ''
            city = city.split(',')[0]
            currency = 'USD'
            source = 'us.despegar.com'
            count += 1
            #sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
        try:
            next = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//div[@class="pagination"]/ul/li[contains(@class, "next")]'))
            next.click()
            banner(driver)
        except:
            driver.quit()
            print '%s, %s, %s hotels, checkin %s, checkout %s, range %s' % (source, city, count, checkin, checkout, date)
            break


if __name__ == '__main__':
    global conn
    global cur
    #conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    #cur = conn.cursor()
    url = 'https://www.us.despegar.com/hotels/'
    scrape_dates()
    #conn.close()


