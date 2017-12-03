#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, os, traceback, re


class BookingScraper(BaseScraper):
    def __init__(self, url, spider):
        BaseScraper.__init__(self, url, spider)
        self.currency = 'GTQ'
        self.source = 'booking.com'
        self.banners = [
            './/div[contains(@class, "close")]',
        ]
        self.base_func()        

    def main_page(self):
        self.checkin_checkout = './/table[contains(@class, "c2-month-table")][./thead/tr/th[contains(text(), "{}")]]/tbody/tr/td/span[contains(text(), "{}")]'
        self.further = './/div[contains(@class, "c2-button-further")]'
        self.close_banner()
        self.city_element()
        self.checkin_element()
        self.checkout_element()
        self.occupancy_element()
        self.submit_element()
        self.scrape_pages()

    def scrape_pages(self):
        next = './/a[contains(@class, "paging-next")]'
        while True:
            self._scroll_down()
            hotels = './/div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]'
            x = self.scrape_hotels(hotels)
            check_element = self.presence(self.driver, hotels, 5)

            try:
                _next = self.visibility(self.driver, next, 5)
                _next.click()
                self.wait_for_page_to_load(check_element)
            except Exception, e:
#                traceback.print_exc()
                self.report()
                break

    def scrape_hotels(self, elements):
        elements = self.elements(self.driver, elements)

        for element in elements:
            self.count += 1
            self.name = self.scrape_name(element)
            self.new_price = self.scrape_new_price(element)
            self.old_price = self.scrape_old_price(element)
            self.review = self.scrape_review(element)
            self.rating = self.scrape_rating(element)
            self.address = self.scrape_address(element)
            self.sql_write()
#            self.full_report()

        return 0

    def _scroll_down(self):
        _range = 400
        _elements = './/td[contains(@class, "roomPrice sr_discount")]/div/strong[contains(@class, "price scarcity_color")]/b'
        elements = self.elements(self.driver, _elements)
        for x in range(_range):
            self.element(self.driver, '//body').send_keys(Keys.ARROW_DOWN)
            elements_2 = [e for e in elements if len(e.text.strip())!=0]
            if len(elements) == len(elements_2):
                break

            time.sleep(0.1)

        return 0

    def city_element(self):
#        print 'city element...'
        element_before = './/input[@id="ss"]'
        element_before = self.visibility(self.driver, element_before, 5)
        element_before.send_keys(self.city)
        time.sleep(3)
        element_after = './/li[contains(@class, "autocomplete")]'
        element_after = self.visibility(self.driver, element_after, 5)
        element_after.click()

    def checkin_element(self):
#        print 'checkin element...'
        year = self.checkin.strftime('%Y')
        month = self.checkin.strftime('%B')
        month_year = '{} {}'.format(month, year)
        day = self.checkin.day 
        checkin_element = self.checkin_checkout.format(month_year, day)            
        self.checkin_checkout_element(checkin_element)

    def checkout_element(self):
#        print 'checkout element...'
        self.click_elements('.//div[contains(@data-placeholder, "Check-out Date")]') 
  
        year = self.checkout.strftime('%Y')
        month = self.checkout.strftime('%B')
        month_year = '{} {}'.format(month, year)
        day = self.checkout.day
        checkout_element = self.checkin_checkout.format(month_year, day)
        self.checkin_checkout_element(checkout_element)

    def checkin_checkout_element(self, checkin_checkout):
#        print 'checkin checkout element...'
        status = False
        while True:
            time.sleep(5)
            _elements = self.elements(self.driver, checkin_checkout)
            for element in _elements:
                try:
                    element.click()
                    status = True
                    break
                except:
                    pass

            if status == True:
                break

            _further = self.elements(self.driver, self.further)
            for further in _further:
                try:
                    further.click()
                    break
                except:
                    pass

    def occupancy_element(self):
#        print 'occupancy element...'
        element = './/select[@name="group_adults"]/option[contains(@value, "1")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def submit_element(self):
#        print 'submit element...'
        element = '//button[@type="submit"]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def scrape_name(self, element): 
        _element = './/span[contains(@class, "sr-hotel__name")]'
        return self.presence(element, _element, 5).text

    def scrape_address(self, element):
        return ''

    def scrape_new_price(self, element):
        try:
            _element = './/td[contains(@class, "roomPrice sr_discount")]/div/strong/b'
            _element = self.visibility(element, _element, 2)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
            _element = _element.strip()
            _element = re.findall(r'([0-9,]+)', _element)[0]
            _element = re.sub(r',', '', _element)
            return int(_element)/3
        except:
            return 0

    def scrape_old_price(self, element):
        try:
            _element = './/span[contains(@data-deal-rack, "rackrate")]'
            _element = self.visibility(element, _element, 2)
            _element = self.driver.execute_script('return arguments[0].innerHTML', _element)
            _element = _element.strip()
            _element = re.findall(r'([0-9,]+)', _element)[0]
            _element = re.sub(r',', '', _element)
            return int(_element)/3
        except:
            return 0

    def scrape_rating(self, element):
        try:
            _element = './/span[contains(@class, "review-score-badge")]'
            _element = self.presence(element, _element, 2).text.strip()
            return _element
        except:
            return 0

    def scrape_review(self, element):
        try: 
            _element = './/span[contains(@class, "review-score-widget__subtext")]'
            _element = self.presence(element, _element, 2).text.strip()
            _element = re.findall(r'([0-9,]+)', _element)[0]
            _element = re.sub(r',', '', _element)
            return _element
        except:
            return 0


if __name__ == '__main__':
    spider = 'chrome'
    url = 'https://www.booking.com/'
    BookingScraper(url, spider)



