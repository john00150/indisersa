import pyodbc, time, datetime, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def sql_exec(conn, cur, sql):
    try:
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        #print e
        pass

class scroll_down(object):
    @staticmethod
    def range(driver, ran, delay):
        el = './/body'
        for x in range(ran):
            element = driver.find_element_by_xpath(el)
            element.send_keys(Keys.ARROW_DOWN)
            time.sleep(delay)
            
    @staticmethod
    def bottom(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @staticmethod
    def click_element(driver, ran, el, delay):
        status = None
        for x in range(ran):
            try:
                element = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, el)))
                element.click()
                sys.exit(0)
            except:
                driver.find_element_by_xpath('.//body').send_keys(Keys.ARROW_DOWN)
        
        raise ValueError('error')

class spider(object):
    @staticmethod
    def chrome(url):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        return driver

    @staticmethod
    def chrome_noImages(url):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        return driver

def sql_write(conn, cur, hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date):
    hotel = hotel.replace("'", "''")
    address = address.replace("'", "''")
    city = city.replace("'", "''")
    sql = "insert into hotel_info (hotel_name, hotel_rating, hotel_review, hotel_address, new_price, old_price, checkin, checkout, city, currency, source, date_scraped, hotel_position, date_range) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)" % (hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, datetime.now().strftime('%m/%d/%Y'), count, date)
    sql_exec(conn, cur, sql)

def csv_write(fh, name, review, rating, address, currency, new_price, old_price, checkin, checkout, city, source):
        line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, review, rating, address, currency, new_price, old_price, checkin, checkout, city, source)
        fh.write(line.encode('utf8'))

def close_banner(driver, banners):
    for banner in banners:
        try:
            element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, banner)))
            element.click()
        except:
            pass


