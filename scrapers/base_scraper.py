from __future__ import print_function
import pyodbc, time, datetime, sys, traceback, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import dates, hostname
from datetime import datetime, timedelta

class BaseScraper(object):
    def __init__(self):
        if hostname != 'john-Vostro-3558':
            self.connect_sql()

        self.dates = dates

        self.main_function()

        if hostname != 'john-Vostro-3558':
            self.close_sql()

    def main_function(self):
        for date in self.dates:
            self.date = date
            self.checkin, self.checkin2 = self.get_checkin()
            self.checkout, self.checkout2 = self.get_checkout()

            for city in self.cities:
                self.city, self.city2 = self.get_city(city)
                self.count = 0

                #if self.spider_name == 'chrome':
                self.driver = self.chrome()
                #if self.spider_name == 'firefox':
                #    self.driver = self.firefox()
                #if self.spider_name == 'chrome_long_window':
                #    self.driver = self.chrome_long_window()

                self.city_element()
                time.sleep(3)
                self.checkin_element()
                time.sleep(3)
                self.checkout_element()
                time.sleep(3)
                self.occupancy_element()
                time.sleep(3)
                self.submit_element()
                time.sleep(3)
                self.scrape_pages()
                self.report()

                self.driver.quit()

    def firefox(self):
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def chrome(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def get_city(self, city):
        return city, city.split(',')[0]

    def presence(self, driver, element, delay):
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, element)))

    def visibility(self, driver, element, delay):
        return WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, element)))

    def clickable(self, driver, element):
        for x in range(50):
            try:
                self.element(self.driver, element).click()
                break
            except:
                time.sleep(0.2)

    def elements(self, driver, elements):
        return driver.find_elements_by_xpath(elements)

    def element(self, driver, element):
        return driver.find_element_by_xpath(element)

    def click_elements(self, elements):
        elements = self.elements(self.driver, elements)
        time.sleep(2)
        for element in elements:
            try:
                element.click()
                break
            except Exception as e:
                time.sleep(1)

    def wait_for_page_to_load(self, element):
        while True:
            try:
                self.element(element, './/a')
                time.sleep(0.2)
            except:
                break

        return 0

    def wait_for_window(self, delay):
        WebDriverWait(self.driver, delay).until(lambda x: len(self.driver.window_handles) > 1)

    def switch_windows(self, delay, number):
        self.wait_for_window(delay)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[number])

    def get_checkin(self):
        checkin = datetime.now() + timedelta(self.date)
        checkin2 = checkin.strftime('%m/%d/%Y')
        return checkin, checkin2

    def get_checkout(self):
        checkout = datetime.now() + timedelta(self.date) + timedelta(3)
        checkout2 = checkout.strftime('%m/%d/%Y')
        return checkout, checkout2

    def close_banner(self):
        for banner in self.banners:
            try:
                self.visibility(self.driver, banner, 2).click()
            except:
                pass

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_click(self, element, _range, delay):
        for x in range(_range):
            try:
                self.element(self.driver, element).click()
                break
            except:
                self.element(self.driver, './/body').send_keys(Keys.ARROW_DOWN)
                time.sleep(delay)

            if x == _range - 1:
                raise ValueError()

    def scroll_to_element(self, _range, element):
        for x in range(_range):
            try:
                self.element(self.driver, element)
                break
            except:
                self.element(self.driver, './/body').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)

    def scroll_range(self, _range):
        for x in range(_range):
            self.element(self.driver, './/body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)

    def scrape_hotels(self, elements):
        for element in elements:
            self.count += 1

            t = (
                self.scrape_name(element).encode('utf8'),
                self.scrape_rating(element),
                self.scrape_review(element), 
                self.scrape_address(element).encode('utf8'),
                self.scrape_new_price(element),
                self.scrape_old_price(element),
                self.checkin2, 
                self.checkout2, 
                self.city2, 
                self.currency, 
                self.source, 
                datetime.now().strftime('%m/%d/%Y'), 
                self.count, 
                self.date
            )

            self.write_sql(t)
            if self.mode == 'print': 
                t = [str(x) for x in t]
                t = '|'.join(t)
                print(t)                

    def connect_sql(self):
        self.conn = pyodbc.connect(
            r"""DRIVER={SQL Server};
            SERVER=(local);
            DATABASE=hotels;
            Trusted_Connection=Yes;
            CharacterSet=UTF-8;"""
        )
        self.cur = self.conn.cursor()

    def write_sql(self, t):
        sql = """INSERT INTO hotel_info (
            hotel_name, 
            hotel_rating, 
            hotel_review, 
            hotel_address,
            new_price, 
            old_price, 
            checkin, 
            checkout, 
            city, 
            currency, 
            source, 
            date_scraped,
            hotel_position, 
            date_range
        ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""

        if hostname != 'john-Vostro-3558':
            try:
                self.cur.execute(sql % t)
                self.conn.commit()
            except Exception as e:
                print(sql)
                traceback.print_exc()           

    def close_sql(self):
        self.conn.close()

    def full_report(self):
        fh = open('report.csv', 'w')
        for t in self.data:
            line = """%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n""" % t
            fh.write(line) 

        fh.close()

    def report(self):
        print ("{}, {}, {} hotels, checkin {}, checkout {}, range {}\n".format(
            self.source, 
            self.city2, 
            self.count, 
            self.checkin2, 
            self.checkout2, 
            self.date
        ))

