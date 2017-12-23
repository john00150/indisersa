from base_scraper import BaseScraper
import time, re


class ElconventoantiguaScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name):
        self.currency = 'USD'
        self.source = 'elconventoantigua.com'
        self.name = 'Convento Boutique Hotel'
        self.address = '2a Avenida Norte #11, Antigua Guatemala +502 7720 7272'
        self.banners = []
        BaseScraper.__init__(self, url, spider, scraper_name)
        self.cities = [self.cities[1]]
    
#    def main_page(self):
#        self.checkin_checkout_element = './/table[@class="ui-datepicker-calendar"]/tbody/tr/td[@data-handler="selectDay"][@data-month="{}"][@data-year="{}"]/a[contains(text(), "{}")]'
#        self.further_element = './/a[contains(@class, "ui-datepicker-next")]'
#        self.checkin_element()
#        self.checkout_element()
#        self.occupancy_element()
#        self.room_element()
#        self.submit_element()
#        self.switch_windows(10, 0)
#        self.scrape_rooms()

    def scrape_rooms(self):
        element = self.get_room_elements()

        self.new_price = self.scrape_new_price(element)
        self.old_price = '0'
        self.rating = '0'
        self.review = '0'
        self.count += 1
        self.sql_write()
        self.report()

    def get_room_elements(self):
        try:
            element = './/div[contains(@class, "AccommodationsList")]/div'
            return self.visibility(self.driver, element, 10)
        except:
            return 1

    def scrape_new_price(self, element):
        if element == 1:
            return 0
        else:
            _element = './/div[contains(@class, "CardList-price-title")]'
            _element = self.element(element, _element)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
            return re.findall(r'([0-9.]+)', _element)[0]

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

    def room_element(self):
        element = './/select[@id="rooms"]/option[contains(text(), "1")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def submit_element(self):
        element = './/button[@type="submit"]'
        element = self.presence(self.driver, element, 10)
        element.click()
        self.switch_windows(10, 0)


if __name__ == "__main__":
    url = 'http://www.elconventoantigua.com/suites-convento-boutique-hotel-,rooms-en.html'
    ElconventoantiguaScraper(url, 'chrome', 'elconventoantigua_scraper')

