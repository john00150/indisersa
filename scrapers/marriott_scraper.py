#encoding: utf8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write, spider, close_banner
import pyodbc, time
from datetime import datetime, timedelta


dates = [15, 30, 60, 90, 120]

address = '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'
city = 'Guatemala City, Guatemala'
source = 'marriott.com'
currency = 'USD'
name = 'Courtyard Guatemala City'
rating = 0

def scrape_price(element):
    new_price = './/div[contains(@class, "t-price")]/span'
    new_price = element.find_element_by_xpath(new_price).text.strip()
    old_price = 0
    return new_price, old_price

def scrape_review(element):
    reviews_element = './/span[contains(text(), "Reviews")]'
    return element.find_element_by_xpath(reviews_element).text.strip()

def scrape_dates():
    for date in dates:
        scrape_hotel(url, date)

def checkin_checkout_scrape(driver, els, next_els):
    x = False
    
    while True:
        try:
            elements = driver.find_elements_by_xpath(els)
            for el in elements:
                try:
                    time.sleep(2)
                    el.click()
                    x = True
                    break
                except:
                    pass
                
            if x == True:
                break
            else:
                raise ValueError()
        except:
            next_elements = driver.find_elements_by_xpath(next_els)
            for el in next_elements:
                try:
                    el.click()
                except:
                    pass

def scrape_hotel(url, date):
    driver = spider.chrome_noImages(url)

    review = scrape_review(driver)

    # input
    input_els = './/input[contains(@class, "js-date-from")]'

    if len(driver.find_elements_by_xpath(input_els)) == 10:
        input_els = './/span[contains(@class, "l-close-icon")]'
    else:
        pass

    input_elements = driver.find_elements_by_xpath(input_els)
    for x in input_elements:
        try:
            x.click()
            break
        except:
            pass

    checkin_checkout_el ='.//div[@aria-label="{}"]'

    # checkin
    checkin = datetime.now() + timedelta(date)
    day = checkin.strftime('%A')[:3]
    month = checkin.strftime('%B')[:3]
    str1 = '{}, {} {}, {}'.format(day, month, checkin.day, checkin.year)
    checkin_elms = checkin_checkout_el.format(str1)
    next_elms = './/div[@title="Next month"]'

    checkin_checkout_scrape(driver, checkin_elms, next_elms)
        
    # checkout
    checkout = datetime.now() + timedelta(date + 3)
    day2 = checkout.strftime('%A')[:3]
    month2 = checkout.strftime('%B')[:3]
    str2 = '{}, {} {}, {}'.format(day2, month2, checkout.day, checkout.year)
    checkout_elms = checkin_checkout_el.format(str2)

    checkin_checkout_scrape(driver, checkout_elms, next_elms)

    review = scrape_review(driver)

    # submit
    submit_els = './/button[contains(@type, "submit")]'
    submit_elements = driver.find_elements_by_xpath(submit_els)
    
    for x in submit_elements:
        try:
            x.click()
            break
        except:
            pass

    try:
        scrape_rooms(driver, checkin, checkout, review, date)
    except:
        pass

    driver.quit()

def scrape_rooms(driver, checkin, checkout, review, date):
    checkin = checkin.strftime('%m/%d/%Y')
    checkout = checkout.strftime('%m/%d/%Y')
    
    room_el = './/div[contains(@class, "results-container")]/div[contains(@class, "m-room-rate-results")]'
    room_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, room_el)))
    
    new_price, old_price = scrape_price(room_element)
    
    sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, 1, date)
    print '{}, checkin {}, checkout {}, range {}'.format(source, checkin, checkout, date)



if __name__ == '__main__':
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    url = 'http://www.marriott.com/hotels/travel/guacy-courtyard-guatemala-city/'
    scrape_dates()
    conn.close()


