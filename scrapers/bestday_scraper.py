#encoding: utf8
from __future__ import print_function
from base_scraper import BaseScraper
from selenium.webdriver.common.keys import Keys
from settings import cities
import time, sys


class BestDayScraper(BaseScraper):
    def __init__(self, mode):
        self.url = 'https://www.bestday.com/Hotels/'
        self.currency = 'USD'
        self.cities = cities
        self.source = 'bestday.com'
        self.mode = mode
        self.banners = []
        BaseScraper.__init__(self)

    def scrape_pages(self):
        _element = './/span[contains(text(), "See more options")]'

        while True:
            try:
                self.presence(self.driver, _element, 20).click()
            except:
                break

        elements = './/ul[@id="hotelList"]/li[contains(@class, "hotel-item")]'
        self.presence(self.driver, elements, 10)
        elements = self.elements(self.driver, elements)
        self.scrape_hotels(elements) 

    def city_element(self):
        if self.city == 'Guatemala City, Guatemala':
            keys = 'Guatemala City'
            element = './/ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]'

        else:
            keys = self.city
            element = './/ul[contains(@class, "ui-autocomplete")]/li[@class="ui-menu-item"]/a[contains(text(), "Antigua, Guatemala")]'

        city_element = './/input[@name="ajhoteles"]'
        city_element = self.presence(self.driver, city_element, 10)
        city_element.send_keys(keys)

        city_dropdown_element = self.visibility(self.driver, element, 10)
        city_dropdown_element.click()

    def checkin_element(self):
        element = '//input[@name="check-inH"]'
        self._next = '//span[@id="nextCalendar"]'
        self.checkin_checkout_element = './/div[./div[contains(@class, "ui-datepicker-header")]/div/span[contains(text(),\
            "{}")]]/table[@class="ui-datepicker-calendar"]/tbody/tr/td/a[contains(text(), "{}")]'

        _element = self.visibility(self.driver, element, 10)
        _element.click()

        while True:
            try:
                self.presence(
                    self.driver, self.checkin_checkout_element.format(self.checkin.strftime('%B'), self.checkin.day), 2
                ).click()
                break
            except Exception as e:
                self.presence(self.driver, self._next, 2).click()
    
    def checkout_element(self):
        while True:
            try:
                self.presence(
                    self.driver, self.checkin_checkout_element.format(self.checkout.strftime('%B'), self.checkout.day), 2
                ).click()
                break
            except Exception as e:
                self.presence(self.driver, self._next, 2).click()

    def occupancy_element(self):
        element = './/select[@name="num_adultos"]/option[contains(@value, "1")]'
        _element = self.visibility(self.driver, element, 10)
        _element.click()

    def submit_element(self):
        element = './/button[@id="btnSubmitHotels"]'
        _element = self.visibility(self.driver, element, 10)
        _element.click()

    def scrape_name(self, element):
        _element = './/a[@class="hotel-name"]'
        return self.element(element, _element).text.strip()

    def scrape_rating(self, element):
        _element = './/span[@class="reviews"]'

        try:
            return self.element(element, _element).text.strip()
        except:
            return 0

    def scrape_address(self, element):
        _element = './/div[@class="details"]/a/span'
        return self.element(element, _element).text.strip()

    def scrape_new_price(self, element):
        _element = './/span[@class="currency"]/span[@class="currency-price"]'

        try:
            price = self.element(element, _element).text.strip()
            #print(price)
            return price
        except:
            return 0

    def scrape_old_price(self, element):
        _element = './/span[@class="currency-before"]/span[@class="currency-before"]/span[@class="currency-price"]'

        try:
            price = self.element(element, _element).text.strip()
            #print(price)
            return price
        except:
            return 0

    def scrape_review(self, element):
        return 0


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
    except:
        mode = ''

    BestDayScraper(mode)

