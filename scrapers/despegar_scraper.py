#encoding: utf8
from base_scraper import BaseScraper
import time, sys, re


class DespegarScraper(BaseScraper):
    def __init__(self, url, spider, scraper_name, city_mode):
        self.currency = 'USD'
        self.source = 'us.despegar.com'
        self.banners = [
            './/i[@class="nevo-modal-close nevo-icon-close"]',
            './/span[contains(@class, "eva-close")]',
        ]
        BaseScraper.__init__(self, url, spider, scraper_name, city_mode)

    def scrape_pages(self):
        element = './/div[contains(@id, "hotels")]/div[contains(@class, "results-cluster-container")]'
        next_element = './/a[@data-ga-el="next"]'
        self.close_banner()

        while True:
            check_element = self.presence(self.driver, element, 10)
            x = self.scrape_hotels(element, 'm')    
#            self.scroll_to_bottom()
        
            try:
                self.visibility(self.driver, next_element, 5).click()
                self.wait_for_page_to_load(check_element)
            except:
                self.driver.quit()
                self.report()
                break

    def city_element(self):
        self.close_banner()

        element = './/input[contains(@class, "sbox-destination")]'
        element = self.presence(self.driver, element, 10)
        
        if self.city == 'Antigua Guatemala, Guatemala':
            element.send_keys('Antigua, Sacatepequez, Guatemala')
        else:
            element.send_keys(self.city)

        element = './/div[@class="geo-searchbox-autocomplete-holder-transition"]'
        if self.city == 'Guatemala City, Guatemala':
            element2 = './/*[contains(., "Guatemala City, Guatemala, Guatemala")]'

        if self.city == 'Antigua Guatemala, Guatemala':
            element2 = './/*[contains(., "Antigua, Sacatepequez, Guatemala")]'
        
        while True:
            try:
                _element = self.presence(self.driver, element, 10)
                _element = self.elements(_element, element2)[1]
                _element.click()
                break
            except:
                pass

    def checkin_checkout_scrape(self, date):
        elements = './/div[contains(@data-month, "{}")]/div/span[contains(text(), "{}")]'
        next_element = './/div[contains(@class, "dpmg2--controls-next")]'

        x = 0
        elements = elements.format(date.strftime('%Y-%m'), date.day)
        while True:
            _elements = self.elements(self.driver, elements)
            for _element in _elements:
                try:
                    _element.click()
                    x = 1
                    break
                except:
                    pass

            if x == 1:
                break

            _next_element = self.visibility(self.driver, next_element, 5)
            _next_element.click()

    def checkin_element(self):
        element = './/input[contains(@class, "sbox-checkin-date")]'
        element = self.visibility(self.driver, element, 10)
        element.click()
        self.checkin_checkout_scrape(self.checkin)

    def checkout_element(self):
        self.checkin_checkout_scrape(self.checkout)

    def occupancy_element(self):
        element = './/div[contains(@class, "sbox-guests-container")]'
        element = self.presence(self.driver, element, 5)
        element.click()
        element2 = './/a[contains(@class, "icon-minus")]'
        element2 = self.presence(self.driver, element2, 5)
        element2.click()
        element3 = './/div[contains(@class, "full")]'
        element3 = self.presence(self.driver, element3, 5)
        element3.click()

    def submit_element(self):
        element = './/a[contains(@class, "sbox-search")]'
        element = self.visibility(self.driver, element, 5)
        element.click()

    def scrape_name(self, element):
        _element = './/h3[@class="hf-hotel-name"]/a'
        return self.element(element, _element).get_attribute('title') 

    def scrape_address(self, element):
#        _element = './/li[@class="hf-cluster-distance"]/span'
#        return self.element(element, _element).text.strip()
        return ''

    def scrape_new_price(self, element):
        _element = './div[contains(@class, "analytics")]'
        return self.element(element, _element).get_attribute('data-price')

    def scrape_old_price(self, element):
        try:
            _element = './/span[contains(@class, "pricebox-price-discount")]'
            _element = self.element(element, _element).text
            return re.findall(r'([0-9.]+)', _element)[0]
        except:
            return 0

    def scrape_rating(self, element):
        try:
            _element = './/span[contains(@class, "rating-text")]'
            return self.element(element, _element).text.strip()
        except:
            return 0

    def scrape_review(self, element):
        _element = './/p[contains(@class, "tooltip-text")]'
        return 0
    

if __name__ == '__main__':
    url = 'https://www.us.despegar.com/hotels/'
    DespegarScraper(url, 'chrome', 'despegar_scraper', 2)


