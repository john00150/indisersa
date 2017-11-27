import pyodbc, time, datetime, sys, traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import dates, cities
from datetime import datetime, timedelta

class BaseScraper(object):
    def __init__(self, url):
        self.url = url
        self.dates = dates
        self.cities = cities
        self.conn, self.cur = self.sql_connect()

    def chrome(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def presence(self, driver, element, delay):
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, element)))

    def visibility(self, driver, element, delay):
        return WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, element)))

    def clickable(self, driver, element, delay):
        return WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, element)))

    def elements(self, driver, elements):
        return driver.find_elements_by_xpath(elements)

    def get_checkin(self):
        checkin = datetime.now() + timedelta(self.date)
        checkin2 = checkin.strftime('%m/%d/%Y')
        return checkin, checkin2

    def get_checkout(self):
        checkout = datetime.now() + timedelta(self.date) + timedelta(3)
        checkout2 = checkout.strftime('%m/%d/%Y')
        return checkout, checkout2

    def sql_connect(self):
        conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
        cur = conn.cursor()
        return conn, cur

    def sql_write(self, item):
        item['name'] = item['name'].replace("'", "''")
        item['address'] = item['address'].replace("'", "''").decode('utf8')
        item['date_scraped'] = datetime.now().strftime('%m/%d/%Y')
        item['checkin'] = self.checkin2
        item['checkout'] = self.checkout2
        item['city'] = self.city.replace("'", "''")
        
#        print "hotel: {}; rating: {}; review: {}; address: {}; new price: {}; old price: {}; checkin: {}; checkout: {};\
#               city: {}; currency: {}; source: {}; count: {}; range: {}"\
#              .format(item['name'.encode('utf8'), item['rating'], item['review'], item['address'].encode('utf8'), item['new_price'],\
#              item['old_price'], item['checkin'], item['checkout'], item['city'], self.currency, self.source, item['count'], self.date)

        sql = "insert into hotel_info (hotel_name, hotel_rating, hotel_review, hotel_address, new_price, old_price, checkin, checkout, city,\
            currency, source, date_scraped, hotel_position, date_range) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', %s)"
            
        self.sql_exec(sql, item)

    def report(self, count):
        print "{}, {}, {} hotels, checkin {}, checkout {}, range {}".format(self.source, self.city.encode('utf8'), count, self.checkin2, self.checkout2, self.date)

    def sql_exec(self, sql, item):
        try:
            self.cur.execute(sql % (item['name'].decode('utf8'), item['rating'], item['review'], item['address'].decode('utf8'), item['new_price'],\
                item['old_price'], self.checkin2, self.checkout2, item['city'], self.currency, self.source, item['date_scraped'], item['count'], self.date))
            
            self.conn.commit()
        except Exception, e:
            pass

    def close_banner(self):
        for banner in self.banners:
            try:
                self.visibility(self.driver, banner, 5).click()
            except:
                pass

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        
