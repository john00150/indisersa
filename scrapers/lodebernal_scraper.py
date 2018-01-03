#encoding: utf8
from base_scraper import BaseScraper
from selenium.webdriver.common.keys import Keys
import time, re


class LodebernalScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name, city_mode, mode):
        self.banners = []
        self.source = 'lodebernal.com'
        self.currency = 'GTQ'
        BaseScraper.__init__(self, url, spider, scraper_name, city_mode, mode)

    def scrape_pages(self):
        try:
            element = './/div[@class="room"]'
            x = self.scrape_hotels(element, 's')
            self.report()
        except:
            pass

    def city_element(self):
        pass

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

    def occupancy_element(self):
        pass

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

    def scrape_name(self, element):
        return 'Hotel Lo de Bernal'

    def scrape_address(self, element):
        return '1. Calle Poniente 23'

    def scrape_review(self, element):
        return 0

    def scrape_rating(self, element):
        return 0

    def scrape_new_price(self, element):
        _element = './/div[contains(@class, "rate_basic_derived")]'
        element = self.presence(element, _element, 20)
        element = self.driver.execute_script('return arguments[0].innerHTML', element)
        element = re.findall(r'([0-9,]+)', element)[0]
        element = re.sub(r',', '', element)
        return int(element)/3 

    def scrape_old_price(self, element):
        return 0
        

if __name__ == "__main__":
    try:
        mode = sys.argv[1]
    except:
        mode = ''

    url = 'http://www.lodebernal.com/'
    LodebernalScraper(url, 'chrome', 'lodebernal_scraper', 1, mode)

