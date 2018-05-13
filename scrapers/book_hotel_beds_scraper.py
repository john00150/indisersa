#encoding: utf8
from base_scraper import BaseScraper
from selenium.webdriver.common.keys import Keys
from settings import cities
import time, os, re, sys


class BookHotelBedsScraper(BaseScraper):
    def __init__(self, mode):
        self.currency = 'GTQ'
        self.url = 'http://www.book-hotel-beds.com/'
        self.mode = mode
        self.citis = cities
        self.source = 'book-hotel-beds.com'
        self.banners = []
        BaseScraper.__init__(self)

    def scrape_pages(self):
        next_element = './/a[contains(text(), "Next")]'
        elements = './/div[@class="hc_sri hc_m_v4"]'
#        element = './/div[@class="hc_sr_summary"]/div[@class="hc_sri hc_m_v4"]'

        while True:
            time.sleep(20)
            check_element = self.presence(self.driver, elements, 10)
            self.presence(self.driver, elements, 10)
            elements = self.elements(self.driver, elements)
            x = self.scrape_hotels(elements)

            try:
                self.visibility(self.driver, next_element, 5).click()
                self.wait_for_page_to_load(check_element)
            except Exception, e:
                self.report()
                break

    def city_element(self):
        element = './/div[@class="hcsb_citySearchWrapper"]/input'
        element = self.visibility(self.driver, element, 10)
        element.send_keys(self.city)

        element = './/ul[@id="ui-id-1"]/li' 
        element = self.visibility(self.driver, element, 10)
        element.click()
    
    def checkin_element(self):
        element = './/body'
        element = self.element(self.driver, element)
        element.click()

        checkin_year_month = '{}-{}'.format(self.checkin.year, self.checkin.month)

        element = '//select[@class="hcsb_checkinMonth"]/option[@value="{}"]'.format(checkin_year_month)
        element = self.visibility(self.driver, element, 10)
        element.click()
    
        element = '//select[@class="hcsb_checkinDay"]/option[@value="{}"]'.format(self.checkin.day)
        element = self.visibility(self.driver, element, 10)
        element.click()

    def checkout_element(self):
        checkout_year_month = '{}-{}'.format(self.checkout.year, self.checkout.month)

        element = '//select[@class="hcsb_checkoutMonth"]/option[@value="{}"]'.format(checkout_year_month)
        element = self.visibility(self.driver, element, 10)
        element.click()
    
        element = '//select[@class="hcsb_checkoutDay"]/option[@value="{}"]'.format(self.checkout.day)
        element = self.visibility(self.driver, element, 10)
        element.click()

    def occupancy_element(self):
        element = './/select[@class="hcsb_guests"]/option[@value="1-1"]'
        element = self.visibility(self.driver, element, 10)
        element.click()

    def submit_element(self):
        element = '//a[@class="hcsb_searchButton"]'
        element = self.visibility(self.driver, element, 10)
        element.click()
        self.switch_windows(10, 0)

    def scrape_address(self, element):
        try:
            _element = './/p[contains(@class, "hc_hotel_location")]'
            return self.visibility(element, _element, 2).text
        except:
            return 0

    def scrape_name(self, element):
        _element = './/a[contains(@data-ceid, "searchresult_hotelname")]'
        return self.element(element, _element).get_attribute('title')

    def scrape_new_price(self, element):
        _element = './/p[contains(@class, "hc_hotel_price")]'
        element = self.element(element, _element).text
        element = re.findall(r'([0-9,]+)', element)[0]
        element = re.sub(r',', '', element)
        return int(element) / 3
    
    def scrape_old_price(self, element):  
        try:  
            _element = './/p[contains(@class, "hc_hotel_wasPrice")]'
            element = self.element(element, _element).text
            element = re.findall(r'([0-9,]+)', element)[0]
            element = re.sub(r',', '', element)
            return int(element) / 3
        except:
            return 0

    def scrape_rating(self, element):
        try:
            _element = './/p[@class="hc_hotel_userRating"]/a'
            element = self.element(element, _element).text
            return re.findall(r'([0-9.]+)', element)[0]
        except:
            return 0

    def scrape_review(self, element):
        try:
            _element = './/p[contains(@class, "hc_hotel_numberOfReviews")]/span'
            element = self.element(element, _element).text.strip()
            return re.sub(r',', '', element)
        except:
            return 0


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
    except:
        mode = ''

    BookHotelBedsScraper(url, mode)

