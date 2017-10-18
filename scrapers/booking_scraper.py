#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write
import pyodbc, time, os, traceback
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
    try:
        elements = driver.find_elements_by_xpath('.//td[contains(@class, "roomPrice sr_discount")]/div/strong[contains(@class, "price scarcity_color")]/b')
        while True:
            driver.find_element_by_xpath('//body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)
            elements_2 = [e for e in elements if len(e.text.strip())!=0]
            if len(elements) == len(elements_2):
                break
    except:
        for x in range(400):
            driver.find_element_by_xpath('.//body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)

def scrape_name(element): 
    el = './/span[contains(@class, "sr-hotel__name")]'
    element = element.find_element_by_xpath(el).text
    return element

def scrape_address(element):
    el = './/div[@class="address"]/a'
    element = element.find_element_by_xpath(el).text.strip()
    return element

def scrape_price(element):
    try:
        new_price = './/td[contains(@class, "roomPrice sr_discount")]/div/strong/b'
        new_price = element.find_element_by_xpath(new_price).text.strip().strip('GTQ').strip().replace(',', '')
        try:
            old_price = './/td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span'
            old_price = element.find_element_by_xpath(old_price).text.strip().strip('GTQ').strip().replace(',', '')
        except:
            old_price = 0
        return int(new_price)/3, int(old_price)/3
    except:
        return 0, 0

def scrape_rating(element):
    try:
        rating = './/span[@itemprop="ratingValue"]'
        rating = element.find_element_by_xpath(rating).text.strip()
        return rating
    except:
        return 0

def scrape_review(element):
    try:
        review ='.//span[@class="score_from_number_of_reviews"]' 
        review = element.find_element_by_xpath(review).text
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
    
    city_element = './/input[@id="ss"]'
    city_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, city_element)))
    city_element.send_keys(city)
    
    if city == 'Guatemala City, Guatemala':
        city_element = './/li[contains(@data-label, "Guatemala, Guatemala, Guatemala")]' 

    if city == 'Antigua Guatemala, Guatemala':
        city_element = './/li[contains(@data-label, "Antigua Guatemala, Guatemala")]'

    city_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, city_element)))
    city_element.click()

    checkin_checkout_el = './/td[contains(@aria-label, "{}")]'
    further_el = './/div[contains(@class, "c2-button-further")]'

    ##### checkin
    checkin = datetime.now() + timedelta(date)
    line = '{} {}, {} {}'.format(checkin.strftime('%A'), checkin.day, checkin.strftime('%B'), checkin.year)
    checkin_el = checkin_checkout_el.format(line)
    print len(driver.find_elements_by_xpath(checkin_el))
    
    while True:
        try:
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, checkin_el)))
            element.click()
            break
            
        except Exception, e:
            print traceback.print_exc()
            further_element = driver.find_elements_by_xpath(further_el)[0]
            further_element.click()

    element = './/div[@data-placeholder="Check-out Date"]'
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, element)))
    element.click()

    ##### checkout
    checkout = datetime.now() + timedelta(date + 3)
    line = '{} {}, {} {}'.format(checkout.strftime('%A'), checkout.day, checkout.strftime('%B'), checkout.year)
    checkout_el = checkin_checkout_el.format(line)
    
    while True:
        try:
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, checkout_el)))
            element.click()
            break
                
        except Exception, e:
            traceback.print_exc()
            further_element = driver.find_elements_by_xpath(further_el)[1]
            further_element.click() 

    ##### occupancy
    occupancy_element = './/select[@name="group_adults"]/option[contains(@value, "1")]'
    occupancy_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, occupancy_element)))
    occupancy_element.click()

    submit_element = '//button[@type="submit"]'
    submit_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, submit_element)))
    submit_element.click()
    
    get_pages(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    
    driver.quit()

def get_pages(driver, city, checkin, checkout, date):
    count = 0
    while True:
        scroll_down(driver)

        hotels = './/div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]'
        hotels = driver.find_elements_by_xpath(hotels)
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


