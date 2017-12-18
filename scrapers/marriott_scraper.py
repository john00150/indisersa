#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, re, sys


class MarriottScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name):
        self.address = '1Avenida 12-47, Zona 10 Guatemala City, 01010 Guatemala'
        self.source = 'marriott.com'
        self.currency = 'USD'
        self.name = 'Courtyard Guatemala City'
        BaseScraper.__init__(self, url, spider, scraper_name)
        self.cities = [self.cities[0]]

#    def main_page(self):
#        self.review = self.scrape_review()
#        self.rating = self.scrape_rating()
#        self.checkin_element()
#        self.checkout_element()
#        self.submit_element()

    def city_element(self):
        self.review = self.scrape_review()
        self.rating = self.scrape_rating()

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

    def scrape_pages(self):  
        self.new_price = self.scrape_new_price()
        self.old_price = 0
        self.count += 1
        self.sql_write()
        self.report()
        self.full_report()

    def scrape_new_price(self):
        try:
            _element = './/h2[contains(@class, "l-display-inline-block")]'       
            _element = self.presence(self.driver, _element, 10)
            return self.driver.execute_script('return arguments[0].innerHTML', _element).strip()
        except:
            _element = './/h2[contains(text(), "Standard Rates")]/span'
            _element = self.presence(self.driver, _element, 10)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
            return re.findall(r'([0-9]+)', _element)[0]
    
    def scrape_review(self):
#        element = './/span[contains(text(), "Reviews")]'
#        element = self.visibility(self.driver, element, 10).text
#        return re.findall(r'([0-9]+)', element)[0]
        return 0

    def scrape_rating(self):
        return 4.5


if __name__ == '__main__':
#    url = 'https://www.marriott.com/hotels/travel/guacy-courtyard-guatemala-city/'
    url = 'https://www.marriott.com/hotels/hotel-rooms/guacy-courtyard-guatemala-city/'
    MarriottScraper(url, 'chrome', sys.argv[1])

