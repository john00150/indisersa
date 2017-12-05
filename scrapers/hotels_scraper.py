#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, re


class HotelsScraper(BaseScraper):
    def __init__(self, url, spider):
        BaseScraper.__init__(self, url, spider)
        self.banners = [
            './/button[@class="cta widget-overlay-close"]',
            './/button[contains(@class, "cta widget-overlay-close")]',
            './/button[contains(@class, "close")]',
            './/div[@class="widget-query-group widget-query-occupancy"]',
            './/div/span[@class="title"][contains(text(), "Save an extra")]/following-sibling::span[@class="close-button"]',
            './/span[contains(@class, "close")]',
            './/span[contains(@class, "close-icon")]',
            './/button[contains(@class, "cta")]'
        ]
        self.currency = 'USD'
        self.source = 'hotels.com'
        self.base_func()

    def main_page(self):
        self.city_element()
        self.checkin_element()
        self.checkout_element()
        self.occupancy_element()
        self.submit_element()
        self.scrape_pages()

    def scrape_pages(self):
        element_to = './/li[contains(text(), "Travelers also looked at these properties nearby")]'
        self.scroll_to_element(500, element_to)

        element = './/ol[contains(@class, "listings")]/li[contains(@class, "hotel")][not(contains(@class, "expanded-area"))]'
        x = self.scrape_hotels(element)
        self.report()

    def city_element(self):
        element = './/input[@name="q-destination"]'
        element = self.visibility(self.driver, element, 10)
        element.send_keys(self.city)
        element.click()
        self.close_banner()

    def checkin_element(self):
        element = '//input[@name="q-localised-check-in"]'
        element = self.presence(self.driver, element, 10)
        element.clear()
        element.send_keys(self.checkin2)    
        self.close_banner()

    def checkout_element(self):
        element = '//input[@name="q-localised-check-out"]'
        element = self.presence(self.driver, element, 10)
        element.clear()
        element.send_keys(self.checkout2)
        self.close_banner()

    def occupancy_element(self):
        element = './/select[@id="qf-0q-compact-occupancy"]/option[contains(text(), "1 room, 1 adult")]'
        element = self.visibility(self.driver, element, 10)
        element.click()
        self.close_banner()

    def submit_element(self):
        element = './/button[contains(@type, "submit")]'
        element = self.visibility(self.driver, element, 10)
        element.click()

    def scrape_name(self, _element):
        return _element.get_attribute('data-title')

    def scrape_address(self, _element):
        element = './/p[contains(@class, "p-adr")]/span'
        elements = self.elements(_element, element)
        elements = [x.text for x in elements]
        elements = ', '.join(elements)
        return elements

    def scrape_price(self, _element):
        element = './/*[contains(text(), "$")]'
        element = self.elements(_element, element)
        element = [e.text.strip('$') for e in element]
        return element

    def scrape_new_price(self, element):
        elements = self.scrape_price(element)
        if len(elements) > 0:
            return elements[-1]
        else:
            return 0

    def scrape_old_price(self, element):
        elements = self.scrape_price(element)
        if len(elements) == 0 or len(elements) == 1:
            return 0
        else:
            return elements[0]

    def scrape_rating(self, _element):
        try:
            element = './/div[contains(@class, "guest-rating")]'
            element = self.presence(_element, element, 2).text
            element = re.findall(r'([0-9.]+)', element)[0]
            return element
        except:
            return 0

    def scrape_review(self, _element):
        try:
            element = './/span[contains(@class, "total-reviews")]'
            element = self.presence(_element, element, 2).text
            element = re.findall(r'([0-9,]+)', element)[0]
            element = re.sub(r',', '', element)
            return element
        except:
            return 0


if __name__ == '__main__':
    spider = 'chrome'
    url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    HotelsScraper(url, spider)


