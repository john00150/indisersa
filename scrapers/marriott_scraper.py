#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, re, sys


class MarriottScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name, city_mode):
        self.source = 'marriott.com'
        self.currency = 'USD'
        BaseScraper.__init__(self, url, spider, scraper_name, city_mode)

    def scrape_pages(self):
        element = './/div'
        x = self.scrape_hotels(element, 's')
        self.report()

    def city_element(self):
        pass

    def checkin_element(self):
        self.checkin_checkout_element ='.//div[@aria-label="{}"]'
        self.further_element = './/div[@title="Next month"]'
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

    def occupancy_element(self):
        pass

    def submit_element(self):
        element = './/button[contains(@type, "submit")]'
        self.presence(self.driver, element, 10)
        elements = self.elements(self.driver, element)
        for element in elements:
            try:
                element.click()
            except:
                time.sleep(1)

    def scrape_name(self, element):
        return 'Courtyard Guatemala City'

    def scrape_new_price(self, element):
        try:
            _element = './/h2[contains(@class, "l-display-inline-block")]'       
            _element = self.presence(self.driver, _element, 10)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element).strip()
            return _element
        except:
            _element = './/h2[contains(text(), "Standard Rates")]/span'
            _element = self.presence(self.driver, _element, 10)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
            _element = re.findall(r'([0-9]+)', _element)[0]
            return _element

    def scrape_old_price(self, element):
        return 0
    
    def scrape_review(self, element):
#        element = './/span[contains(text(), "Reviews")]'
#        element = self.visibility(self.driver, element, 10).text
#        return re.findall(r'([0-9]+)', element)[0]
        return 0

    def scrape_rating(self, element):
        return 4.5

    def scrape_address(self, element):
        return '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'


if __name__ == '__main__':
#    url = 'https://www.marriott.com/hotels/travel/guacy-courtyard-guatemala-city/'
    url = 'https://www.marriott.com/hotels/hotel-rooms/guacy-courtyard-guatemala-city/'
    MarriottScraper(url, 'chrome', 'marriott_scraper', 0)

