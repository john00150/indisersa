#encoding: utf8
from selenium.webdriver.common.keys import Keys
from base_scraper import BaseScraper
import time, os, traceback


class BookingScraper(BaseScraper):
    def __init__(self, url):
        BaseScraper.__init__(self, url)
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
        #get_pages()

    def city_element(self):
        element_before = './/input[@id="ss"]'
        element_before = self.visibility(self.driver, element_before, 5)
        element_before.send_keys(self.city)
        time.sleep(3)
        element_after = './/li[contains(@class, "autocomplete")]'
        element_after = self.visibility(self.driver, element_after, 5)
        element_after.click()

    def checkin_element(self):
        year = self.checkin.strftime('%Y')
        month = self.checkin.strftime('%B')
        month_year = '{} {}'.format(month, year)
        day = self.checkin.day 
        checkin_element = self.checkin_checkout.format(month_year, day)            
        self.checkin_checkout_element(checkin_element)

    def checkout_element(self):
        element = './/div[@data-placeholder="Check-out Date"]'
        element = self.visibility(self.driver, element, 5)
        element.click()
    
        year = self.checkout.strftime('%Y')
        month = self.checkout.strftime('%B')
        month_year = '{} {}'.format(month, year)
        day = self.checkout.day
        checkout_element = self.checkin_checkout.format(month_year, day)
        self.checkin_checkout_element(checkout_element)

    def checkin_checkout_element(self, checkin_checkout):
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

            _further = self.elements(self.further)
            for further in _further:
                try:
                    further.click()
                    break
                except:
                    pass

    def occupancy_element(self):
        element = './/select[@name="group_adults"]/option[contains(@value, "1")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def submit_element(self):
        element = '//button[@type="submit"]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def get_pages(driver, city, checkin, checkout, date):
        count = 0
        while True:
            next_el = './/a[contains(@class, "paging-next")]'
            _scroll_down(driver)
            ###print 'scroll 1'
    
#            hotels = './/div[@id="hotellist_inner"]/div[contains(@class, "sr_item")]'
#            hotels = driver.find_elements_by_xpath(hotels)
#            for hotel in hotels:
#                count += 1
#                name = scrape_name(hotel)
#                new_price, old_price = scrape_price(hotel)
#                review = scrape_review(hotel)
#                rating = scrape_rating(hotel)
#                address = ''
#                city = city.split(',')[0]

#                _db.sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, count, date)
            
#            time.sleep(30)
        
            try:
                scroll_down.til_clickable(driver, 500, next_el, 5, 0.4)
            except Exception, e:
                #print traceback.print_exc()
                driver.quit()
                self.report()
                break

    def _scroll_down(self):
        _elements = './/td[contains(@class, "roomPrice sr_discount")]/div/strong[contains(@class, "price scarcity_color")]/b'
        try:
            elements = self.elements(_elements)
            while True:
                self.element(self.driver, '//body').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.4)
                elements_2 = [e for e in elements if len(e.text.strip())!=0]
                if len(elements) == len(elements_2):
                    break
        except:
            for x in range(400):
                self.element(self.driver, './/body').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.4)

    def scrape_name_element(self, element): 
        _element = './/span[contains(@class, "sr-hotel__name")]'
        return self.presence().text

    def scrape_address_element(self, element):
        _element = './/div[@class="address"]/a'
        return self.presence().text.strip()

    def scrape_new_price_element(self, element):
        try:
            new_price = './/td[contains(@class, "roomPrice sr_discount")]/div/strong/b'
            new_price = element.find_element_by_xpath(new_price).text.strip().strip('GTQ').strip().replace(',', '')
            try:
                old_price = './/td[contains(@class, "roomPrice sr_discount")]/div/span[@class="strike-it-red_anim"]/span'
                old_price = element.find_element_by_xpath(old_price).text.strip().strip('GTQ').strip().replace(',', '')
            except:
                old_price = 0
            return int(new_price)/3, int(old_price)/3
        except:
            return 0, 0

    def scrape_old_price_element(self):
        return self.presence()

    def scrape_rating_element(self, element):
        _element = './/span[@itemprop="ratingValue"]'
        return self.presence(element).text.strip()

    def scrape_review_element(self, element):
        element ='.//span[@class="score_from_number_of_reviews"]' 
        return self.presence().text.strip()


if __name__ == '__main__':
    url = 'https://www.booking.com/'
    BookingScraper(url)



