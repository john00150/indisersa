import pyodbc, time, datetime, sys, traceback, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import dates, cities
from datetime import datetime, timedelta

class BaseScraper(object):
    def __init__(self, url, spider_name, scraper_name):
        self.data = []
        self.spider_name = spider_name
        self.scraper_name = scraper_name
        self.url = url
        self.dates = dates
        self.cities = cities
        self.main_function()
        self._sql()
#        self.full_report()

    def main_function(self):
        for date in self.dates:
            self.date = date
            self.checkin, self.checkin2 = self.get_checkin()
            self.checkout, self.checkout2 = self.get_checkout()

            for city in self.cities:
                self.city, self.city2 = self.get_city(city)
                self.count = 0

                if self.spider_name == 'chrome':
                    self.driver = self.chrome()
                if self.spider_name == 'firefox':
                    self.driver = self.firefox()
                if self.spider_name == 'chrome_long_window':
                    self.driver = self.chrome_long_window()

                self.main_page()
                self.driver.quit()

    def main_page(self):
        self.error_func(self.city_element, 'city_element')
        self.error_func(self.checkin_element, 'checkin_element')
        self.error_func(self.checkout_element, 'checkout_element')
        self.error_func(self.occupancy_element, 'occupancy_element')
        self.error_func(self.submit_element, 'submit_element')
        self.error_func(self.scrape_pages, 'scrape_pages')

    def error_func(self, function, func_name):
        try:
            function()
        except Exception, e:
            print '########## {} ##########'.format(self.scraper_name)
            print '###        {}        ###'.format(func_name)
            traceback.print_exc()
            print '#########################################'
            raise

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
            except Exception, e:
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
                time.sleep(0.2)

    def scroll_range(self, _range):
        for x in range(_range):
            self.element(self.driver, './/body').send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)

    def scrape_hotels(self, elements):
        self.presence(self.driver, elements, 10)
        elements = self.elements(self.driver, elements)

        for element in elements:
            self.count += 1
            self.data.append((
            self.scrape_name(element),
            self.scrape_rating(element),
            self.scrape_review(element), 
            self.scrape_address(element),
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
            ))

    def _sql(self):
        conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=(local);DATABASE=hotels;Trusted_Connection=Yes;CharacterSet=UTF-8;')
        cur = conn.cursor()

        sql = """insert into hotel_info (
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
            date_range) values(
                "%s", %s, %s, "%s", %s, %s, "%s", "%s", "%s", "%s", "%s", "%s", %s, %s
            )"""

        for t in self.data:            
            try:
                cur.execute(sql, t)
            except Exception, e:
                traceback.print_exc()           
#                pass

        conn.commit()
        conn.close()

    def full_report(self):
        fh = open('report.csv', 'w')
        for t in self.data:
            line = """%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n""" % t
            fh.write(line) 

        fh.close()

    def report(self):
        print "{}, {}, {} hotels, checkin {}, checkout {}, range {}".format(
            self.source, 
            self.city2, 
            self.count, 
            self.checkin2, 
            self.checkout2, 
            self.date
        )

