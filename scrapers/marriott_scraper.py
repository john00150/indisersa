#encoding: utf8
from __future__ import print_function
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
from settings import cities
import time, re, sys


class MarriottScraper(BaseScraper):
    def __init__(self, mode):
        self.url = 'https://www.marriott.com/hotels/hotel-rooms/guacy-courtyard-guatemala-city/'
        self.checkin_checkout_element ='.//div[@aria-label="{}"]'
        self.further_element = './/div[@title="Next month"]'
        self.cities = cities[:1]
        self.mode = mode
        self.source = 'marriott.com'
        self.currency = 'USD'
        self.banners = [
            './/button[contains(@class, "close")]'
        ]
        BaseScraper.__init__(self)

    def scrape_pages(self):
        elements = './/div'
        elements = self.presence(self.driver, elements, 10)
        self.scrape_hotels([elements])

    def city_element(self):
        self.close_banner()

    def checkin_element(self):
        checkin_el = './/input[@placeholder="Check-in"]'

        _str = '{}, {} {}, {}'.format(
            self.checkin.strftime('%A')[:3],
            self.checkin.strftime('%B')[:3],
            self.checkin.day, 
            self.checkin.year
        )

        self.click_date_picker()

        self.elements(self.driver, checkin_el)[2].clear()
        time.sleep(1)

        self.elements(self.driver, checkin_el)[2].send_keys(_str)
        time.sleep(1)

    def checkout_element(self):
        checkout_el = './/input[@placeholder="Check-out"]'

        _str = '{}, {} {}, {}'.format(
            self.checkout.strftime('%A')[:3],
            self.checkout.strftime('%B')[:3],
            self.checkout.day, 
            self.checkout.year
        )

        self.click_date_picker()

        self.elements(self.driver, checkout_el)[2].clear()
        time.sleep(1)

        self.elements(self.driver, checkout_el)[2].send_keys(_str)
        time.sleep(1)

        self.element(self.driver, './/body').click()

    def click_date_picker(self):
        element = './/div[contains(@class, "js-toggle-picker")]'
        self.elements(self.driver, element)[1].click()
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
    try:
        mode = sys.argv[1]
    except:
        mode = ''

    MarriottScraper(mode)

