#encoding: utf8
from base_scraper import BaseScraper
from selenium.webdriver.common.keys import Keys
import time, re


class LodebernalScraper(BaseScraper):
    def __init__(self, url):
        BaseScraper.__init__(self, url)
        self.source = 'lodebernal.com'
        self.city = 'Antigua Guatemala, Guatemala'
        self.currency = 'GTQ'
            
        for date in self.dates:
            self.date = date
            self.checkin, self.checkin2 = self.get_checkin()
            self.checkout, self.checkout2 = self.get_checkout()
            self.driver = self.chrome()
            time.sleep(5)
            self.scrape_checkin()
            self.scrape_checkout()
            self.scrape_submit()
            self.scrape_room(date)
            self.driver.quit()

        self.conn.close()

    def scrape_checkin(self):
        checkin_element = './/div[@class="form_group start_date"]/div/input'
        checkin_element = self.visibility(self.driver, checkin_element, 10)
        self.clear_input(checkin_element)
        checkin_element.send_keys(self.checkin.strftime('%m/%d/%Y'))

    def scrape_checkout(self):
        checkout_element = './/div[@class="form_group end_date"]/div/input'
        checkout_element = self.visibility(self.driver, checkout_element, 10)
        self.clear_input(checkout_element)
        checkout_element.send_keys(self.checkout.strftime('%m/%d/%Y'))

    def scrape_submit(self):
        submit_element = './/input[@value="Search"]'
        submit_element = self.visibility(self.driver, submit_element, 10)
        submit_element.click()
        
    def clear_input(self, element):
        element.click()
        time.sleep(2)
        for x in range(5):
            element.send_keys(Keys.ARROW_RIGHT)

        for x in range(10):
            element.send_keys(Keys.BACK_SPACE)

    def get_price(self):
        element = './/div[@class="room_types"]/div[@class="room"]'
        price = self.presence(self.driver, element, 10)
        price = price.find_elements_by_xpath('.//div[contains(@class, "rate_basic_derived")]')[0]
        price = int(float(re.sub('Q|,| +', '', price.text)))/3   
        return price

    def scrape_room(self, date):
        try:
            item = {}
            item['new_price'] = self.get_price()
            item['old_price'] = 0
            item['name'] = 'Hotel Lo de Bernal'
            item['review'] = ''
            item['rating'] = ''
            item['address'] = '1ª. Calle Poniente 23'
            item['count'] = 1
            self.sql_write(item)
            self.report(item['count'])
        except Exception, e:
            pass
#            print e
        

if __name__ == "__main__":
    url = 'http://www.lodebernal.com/'
    LodebernalScraper(url)

