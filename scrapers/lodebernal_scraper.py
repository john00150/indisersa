#encoding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from processors import sql_write
import pyodbc, time, re
from datetime import datetime, timedelta


f_h = open('lodebernal_prices.txt', 'w')

url = 'http://www.lodebernal.com/'
dates = [15, 30, 60, 90, 120]


def scrape_dates():
    for date in dates:
        scrape_hotel(date)

def clear_input(element):
    element.click()
    time.sleep(2)
    for x in range(5):
        element.send_keys(Keys.ARROW_RIGHT)

    for x in range(10):
        element.send_keys(Keys.BACK_SPACE)

def get_price(driver):
    element = './/div[@class="room_types"]/div[@class="room"]'
    price = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, element)))
    price = price.find_elements_by_xpath('.//div[contains(@class, "rate_basic_derived")]')[0]
    f_h.write(price.text+'\n')
    price = int(float(re.sub('Q|,| +', '', price.text)))/3   
    return price

def scrape_hotel(date):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    checkin = datetime.now() + timedelta(date)
    checkin2 = checkin.strftime('%m/%d/%Y')
    element_1 = driver.find_element_by_xpath('.//div[@class="form_group start_date"]/div/input')
    clear_input(element_1)
    element_1.send_keys(checkin2)
    time.sleep(1)

    checkout = checkin + timedelta(3)
    checkout2 = checkout.strftime('%m/%d/%Y')
    element_2 = driver.find_element_by_xpath('.//div[@class="form_group end_date"]/div/input')
    clear_input(element_2)
    element_2.send_keys(checkout2)
    time.sleep(1)

    driver.find_element_by_xpath('.//input[@value="Search"]').click()
    scrape_room(driver, checkin2, checkout2, date)

def scrape_room(driver, checkin, checkout, date):
    new_price = get_price(driver)
    old_price = 0
    name = 'Hotel Lo de Bernal'
    review = ''
    rating = ''
    address = '1ª. Calle Poniente 23'
    city = 'Antigua Guatemala, Guatemala'
    source = 'lodebernal.com'
    currency = 'GTQ'
    sql_write(conn, cur, name, rating, review, address.decode('utf8'), new_price, old_price, checkin, checkout, city, currency, source, 1, date)
    print '{}, checkin {}, checkout {}, range {}'.format(source, checkin, checkout, date)

    driver.quit()


if __name__ == "__main__":
    global conn
    global cur
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
    cur = conn.cursor()
    scrape_dates()
    conn.close()

f_h.close()
