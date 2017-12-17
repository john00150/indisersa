#encoding: utf8
from base_scraper import BaseScraper
from selenium.webdriver.common.keys import Keys
import time, re


class LodebernalScraper(BaseScraper):
    def __init__(self, url, spider):
        self.banners = []
        self.source = 'lodebernal.com'
        self.cities = [self.cities[1]]
        self.currency = 'GTQ'
        BaseScraper.__init__(self, url, spider)

    def main_page(self):
        self.checkin_element()
        self.checkout_element()
        self.submit_element()
        self.scrape_rooms()

    def checkin_element(self):
        element = './/div[@class="form_group start_date"]/div/input'
        element = self.visibility(self.driver, element, 10)
        self.clear_input(element)
        element.send_keys(self.checkin2)

    def checkout_element(self):
        element = './/div[@class="form_group end_date"]/div/input'
        element = self.visibility(self.driver, element, 10)
        self.clear_input(element)
        element.send_keys(self.checkout2)

    def submit_element(self):
        element = './/input[@value="Search"]'
        element = self.visibility(self.driver, element, 10)
        element.click()
        
    def clear_input(self, element):
        self.clickable(self.driver, element)

        for x in range(5):
            element.send_keys(Keys.ARROW_RIGHT)

        for x in range(10):
            element.send_keys(Keys.BACK_SPACE)

    def scrape_new_price(self, element):
        _element = './/div[contains(@class, "rate_basic_derived")]'
        _element = self.presence(element, _element, 20)
        _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
        _element = re.findall(r'([0-9,]+)', _element)[0]
        _element = re.sub(r',', '', _element)
        _element = int(_element)/3   
        return _element

    def scrape_rooms(self):
        time.sleep(10)
        element = './/div[@class="room"]'
        try:
            element = self.presence(self.driver, element, 10)

            self.new_price = self.scrape_new_price(element)
            self.old_price = 0
            self.name = 'Hotel Lo de Bernal'
            self.review = 0
            self.rating = 0
            self.address = '1. Calle Poniente 23'
            self.count += 1
            self.sql_write()
            self.report()
            self.full_report()
        except Exception, e:
            pass
        

if __name__ == "__main__":
    url = 'http://www.lodebernal.com/'
    spider = 'chrome'
    LodebernalScraper(url, spider)

