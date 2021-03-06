#encoding: utf8
from __future__ import print_function
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
from settings import cities
import time, re, json, sys


class RadissonScraper(BaseScraper):
    def __init__(self, mode):
        self.url = 'https://www.radisson.com/'
        self.cities = cities[:1]
        self.mode = mode 
        self.banners = [
            './/div[@class="cookieControl"]/div/div/table/tbody/tr/td/a[@class="commit"]',
        ]
        self.source = 'radisson.com'
        self.currency = 'GTQ'
        BaseScraper.__init__(self)

    def scrape_pages(self):
        elements = './/div[contains(@class, "hotelRow")]'
        elements = self.presence(self.driver, elements, 10)
        elements = [elements]
#        print self.presence(self.driver, element, 10).get_attribute('hoteldata')
        x = self.scrape_hotels(elements)

    def city_element(self):
        element = './/input[@name="city"]'
        element = self.visibility(self.driver, element, 5)
        element.send_keys(self.city)
        time.sleep(2)
        self.element(self.driver, './/body').click()

    def checkin_element(self):
        self.checkin_checkout_element = './/td[@data-handler="selectDay"][@data-month="{}"][@data-year="{}"]/a[contains(text(), "{}")]'
        self.further_element = './/a[@data-handler="next"]'

        element = './/input[@id="checkinDate"]'
        element = self.visibility(self.driver, element, 5)
        element.click()

        element = self.checkin_checkout_element.format(self.checkin.month-1, self.checkin.year, self.checkin.day)

        while True:
            try:
                _element = self.visibility(self.driver, element, 2)
                _element.click()
                break
            except:
                _further = self.visibility(self.driver, self.further_element, 2)
                _further.click()

    def checkout_element(self):
        element = './/input[@id="checkoutDate"]'
        element = self.visibility(self.driver, element, 5)
        element.click()

        element = self.checkin_checkout_element.format(self.checkout.month-1, self.checkout.year, self.checkout.day)
        while True:
            try:
                _element = self.visibility(self.driver, element, 2)
                _element.click()
                break
            except:
                _further = self.visibility(self.driver, self.further_element, 2)
                _further.click()

    def occupancy_element(self):
        pass

    def submit_element(self):
        element = './/a[contains(@title, "Go")]'
        self.clickable(self.driver, element)

    def scrape_name(self, element):
        element = element.get_attribute('hoteldata')
        return json.loads(element)['hotelName']

    def scrape_address(self, element):
        element = './/td[@id="hoteladdress"]'
        element = self.visibility(self.driver, element, 5).text
        element = element.split('|')[0].strip()
        return re.sub(r'\n', ', ', element)

    def scrape_new_price(self, element):
        return int(json.loads(element.get_attribute('hoteldata'))['price']/3)

    def scrape_old_price(self, element):
        return 0

    def scrape_rating(self, element):
        element = element.get_attribute('hoteldata')
        return json.loads(element)['rating']

    def scrape_review(self, element):
        _element = './/a[@class="ratingLink"]'
        return re.findall(r'([0-9,]+)', self.element(element, _element).text)[0]


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
    except:
        mode = None
 
    RadissonScraper(mode)

