#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time


class MarriottScraper(BaseScraper):
    def __init__(self, url, spider):
        BaseScraper.__init__(self, url, spider)
        self.address = '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'
        self.cities = [self.cities[0]]
        self.source = 'marriott.com'
        self.currency = 'USD'
        self.name = 'Courtyard Guatemala City'

        self.base_func()

    def main_page(self):
        self.checkin_checkout_element ='.//div[@aria-label="{}"]'
        self.further_element = './/div[@title="Next month"]'
        self.checkin_element()
        self.checkout_element()
        self.submit_element()
        self.scrape_rooms()

    def scrape_rooms(self):    
        element = './/div[contains(@class, "room-rate-results rate")]'
        element = self.presence(self.driver, element, 20)
    
        self.new_price = self.scrape_new_price(element)
        self.old_price = 0
        self.review = self.scrape_review()
        self.rating = self.scrape_rating()
        self.count += 1
        self.sql_write()
        self.report()
        self.full_report()

    def checkin_element(self):
        elements = './/span[contains(@class, "l-icon-calendar")]'
        elements = self.elements(self.driver, elements)
        for element in elements:
            try:
                element.click()
                break
            except:
                time.sleep(1)

        _str = '{}, {} {}, {}'.format(
            self.checkin.strftime('%A')[:3],
            self.checkin.strftime('%B')[:3],
            self.checkin.day, 
            self.checkin.year
        )
        elements = self.checkin_checkout_element.format(_str)
        self._checkin_checkout_element(elements)

    def checkout_element(self):
        _str = '{}, {} {}, {}'.format(
            self.checkout.strftime('%A')[:3],
            self.checkout.strftime('%B')[:3],
            self.checkout.day, 
            self.checkout.year
        )
        elements = self.checkin_checkout_element.format(_str)
        self._checkin_checkout_element(elements)
        self.element(self.driver, './/body').click()

    def _checkin_checkout_element(self, elements):
        x = False
    
        while True:
            _elements = self.elements(self.driver, elements)
            for _element in _elements:
                try:
                    _element.click()
                    x = True
                    break
                except:
                    time.sleep(1)
                
            if x == True:
                break
            
            _furthers = self.elements(self.driver, self.further_element)
            for _further in _furthers:
                try:
                    _further.click()
                except:
                    time.sleep(1)

    def submit_element(self):
        element = './/button[contains(@type, "submit")]'
        self.presence(self.driver, element, 10)
        elements = self.elements(self.driver, element)
        for element in elements:
            try:
                element.click()
            except:
                time.sleep(1)

    def scrape_new_price(self, element):
        _element = './/h2[contains(@class, "l-display-inline-block")]'
        _element = self.presence(self.driver, _element, 20)
        _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
        return _element.strip()
        
    
    def scrape_review(self):
        element = './/span[contains(@class, "reviews-count")]'
        element = self.visibility(self.driver, element, 5).text.strip()
        return element

    def scrape_rating(self):
        element = './/span[contains(@class, "user-rating")]'
        element = self.visibility(self.driver, element, 5).text.strip()
        return element


if __name__ == '__main__':
#    url = 'https://www.marriott.com/hotels/travel/guacy-courtyard-guatemala-city/'
    url = 'https://www.marriott.com/hotels/hotel-rooms/guacy-courtyard-guatemala-city/'
    spider = 'chrome'
    MarriottScraper(url, spider)

