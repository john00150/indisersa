from base_scraper import BaseScraper
from settings import cities
import time, re, sys


class ElconventoantiguaScraper(BaseScraper):
    def __init__(self, mode):
        self.url = 'http://www.elconventoantigua.com/suites-convento-boutique-hotel'
        self.mode = mode
        self.cities = cities[1:]
        self.currency = 'USD'
        self.source = 'elconventoantigua.com'
        self.banners = []
        BaseScraper.__init__(self)

    def scrape_pages(self):
        try:
            elements = './/div[contains(@ng-if, "displayMultiRateListView")]'
            elements = self.presence(self.driver, elements, 10)
            self.scrape_hotels([elements])
        except:
            pass

    def scrape_name(self, element):
        return 'Convento Boutique Hotel'

    def scrape_address(self, element):
        return '2a Avenida Norte #11, Antigua Guatemala +502 7720 7272'

    def scrape_new_price(self, element):
        _element = './/div[contains(@class, "CardGrid-price")]'
        _element = self.elements(element, _element)
        _element = [x.text.replace('$', '').strip() for x in _element if '$' in x.text]
        _element.sort()
        return _element[0]

    def scrape_old_price(self, element):
        return 0

    def scrape_rating(self, element):
        return 0

    def scrape_review(self, element):
        return 0

    def city_element(self):
        pass

    def checkin_element(self):
        self.checkin_checkout_element = './/table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="{}"][@data-year="{}"]/a[contains(text(), "{}")]'
        self.further_element = './/a[contains(@class, "ui-datepicker-next")]'

        element = './/input[@id="date-in"]'
        element = self.presence(self.driver, element, 5)
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
        element = './/select[@id="adults"]/option[contains(text(), "1")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

        element = './/select[@id="rooms"]/option[contains(text(), "1")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def submit_element(self):
        element = './/button[@type="submit"]'
        element = self.presence(self.driver, element, 10)
        element.click()
        self.switch_windows(10, 0)


if __name__ == "__main__":
    try:
        mode = sys.argv[1]
    except:
        mode = ''

    ElconventoantiguaScraper(mode)

