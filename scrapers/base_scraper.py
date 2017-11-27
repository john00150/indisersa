import pyodbc, time, datetime, sys, traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pyodbc


class Base_scraper(object):
    def __init__(self, url):
        self.url = url
        self.banners = banners
        self.conn, self.cur = self.connect()

    def spider(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def scrape_dates(self):
        for date in self.dates:
            self.scrape_city(date) 

    def presence(self, element, delay):
        return WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, element)))

    def visibility(self, element, delay):
        return WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, element)))

    def clickable(self, element, delay):
        return WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, element)))

    def find_elements(self, elements):
        return self.driver.find_elements_by_xpath(elements)

    def find_element(self, element):
        return self.driver.find_element_by_xpath(element)

    def close_banner(self):
        for banner in self.banners:
            try:
                element = self.wait_visibility(banner, 5)
                element.click()
            except:
                pass

    def scroll_range(self, ran, delay):
        for x in range(ran):
            element = self.find_element('.//body')
            element.send_keys(Keys.ARROW_DOWN)
            time.sleep(delay)
            
    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_click(self, ran, el, delay):
        status = None
        for x in range(ran):
            try:
                self.visibility(el, delay).click()
                sys.exit(0)
            except:
                self.find_element('.//body').send_keys(Keys.ARROW_DOWN)
        
            raise ValueError('error')

    def scroll_clickable(self, ran, el, delay, delay2):
        try:
            self.visibility(el, delay)
            
            for x in range(ran):
                try:
                    time.sleep(delay2)
                    element = self.visibility(el, delay)
                    element.click()
                    break
                except:
                    self.find_element('.//body').send_keys(Keys.ARROW_DOWN)
            ###print 'click is fine'
        except:
            ###print 'click error'
            raise ValueError()

    def connect(self):
        conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;')
        cur = conn.cursor()
        return conn, cur

    def sql_write(self, hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date):
            hotel = hotel.replace("'", "''")
            address = address.replace("'", "''")
            city = city.replace("'", "''")
            sql = "insert into hotel_info (hotel_name, hotel_rating, hotel_review, hotel_address, new_price, old_price, checkin, checkout, city, currency, source, date_scraped, hotel_position, date_range) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)" % (hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, datetime.now().strftime('%m/%d/%Y'), count, date)
            self.sql_exec(self.conn, self.cur, sql)

    def sql_exec(self, sql):
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception, e:
                pass




