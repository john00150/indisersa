from base_scraper import BaseScraper
import time, re


class ElconventoantiguaScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name, city_mode, mode):
        self.currency = 'USD'
        self.source = 'elconventoantigua.com'
        self.banners = []
        BaseScraper.__init__(self, url, spider, scraper_name, city_mode, mode)

    def scrape_pages(self):
        try:
            element = './/div[contains(@class, "AccommodationsList")]/div'
            x = self.scrape_hotels(element, 's')
            self.report()
        except:
            pass

    def scrape_name(self, element):
        return 'Convento Boutique Hotel'

    def scrape_address(self, element):
        return '2a Avenida Norte #11, Antigua Guatemala +502 7720 7272'

    def scrape_new_price(self, element):
        _element = './/div[contains(@class, "CardList-price-title")]'
        _element = self.element(element, _element)
        _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
        _element = re.findall(r'([0-9.]+)', _element)[0]
        print _element
        return _element

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

    url = 'http://www.elconventoantigua.com/suites-convento-boutique-hotel-,rooms-en.html'
    ElconventoantiguaScraper(url, 'chrome', 'elconventoantigua_scraper', 1, mode)

