#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, re


class RadissonScraper(BaseScraper):
    def __init__(self, url, spider):
        self.banners = [
            './/div[@class="cookieControl"]/div/div/table/tbody/tr/td/a[@class="commit"]',
        ]
        self.source = 'radisson.com'
        self.currency = 'GTQ'
        self.cities = [self.cities[0]]
        BaseScraper.__init__(self, url, spider)

    def main_page(self):
        self.checkin_checkout_element = './/td[@data-handler="selectDay"][@data-month="{}"][@data-year="{}"]/a[contains(text(), "{}")]'
        self.further_element = './/a[@data-handler="next"]'
        self.close_banner()
        self.city_element()
        self.checkin_element()
        self.checkout_element()
        self.submit_element()
        self.scrape_rooms()

    def scrape_rooms(self):
        self.name = self.scrape_name()
        self.new_price = self.scrape_new_price()
        self.old_price = 0
        self.rating = self.scrape_rating()
        self.review = self.scrape_review()
        self.address = self.scrape_address()
        self.count += 1
        self.sql_write()
        self.report()
#        self.full_report()        

    def city_element(self):
        element = './/input[@name="city"]'
        element = self.visibility(self.driver, element, 5)
        element.send_keys(self.city)

    def checkin_element(self):
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

    def submit_element(self):
        element = './/a[contains(@title, "Go")]'
        self.clickable(self.driver, element)

    def scrape_name(self):
        element = './/div[@class="innername"]/a'
        element = self.visibility(self.driver, element, 5).text
        return element.strip()

    def scrape_address(self):
        element = './/td[@id="hoteladdress"]'
        element = self.visibility(self.driver, element, 5).text
        element = element.split('|')[0].strip()
        element = re.sub(r'\n', ',', element)
        return element

    def scrape_location(self):
        element = './/td[@id="hoteladdress"]'
        element = self.visibility(self.driver, element, 5).text
        return element

    def scrape_new_price(self):
        try:
            element = './/td[@class="rateamount"]'
            element = self.visibility(self.driver, element, 5).text
            element = re.sub(r',', '', element)
            return element.strip()
        except:
            return 0

    def scrape_rating(self):
        element = './/img[@class="rating_circles"]'
        element = self.visibility(self.driver, element, 5)
        return element.get_attribute('title')

    def scrape_review(self):
        element = './/a[@class="ratingLink"]'
        element = self.visibility(self.driver, element, 5).text
        element = re.findall(r'([0-9,]+)', element)[0]
        element = re.sub(r',', '', element)
        return element


if __name__ == '__main__': 
    url = 'https://www.radisson.com/' 
    spider = 'chrome'  
    RadissonScraper(url, spider)


