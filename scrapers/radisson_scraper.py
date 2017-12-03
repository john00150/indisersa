#encoding: utf8
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
from settings import cities, dates
from base_scraper import Base_scraper


banners = [
    './/div[@class="cookieControl"]/div/div/table/tbody/tr/td/a[@class="commit"]',
]

url = 'https://www.radisson.com/'

class Radisson_scraper(Base_scraper):
    def __init__(self, url):
        Base_scraper.__init__(self, url)

    def get_name(self):
        return self.WebDriverWait(element, 10).until(lambda'.//div[@class="innername"]/a').text.strip())

    def get_address(self):
        return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[0].strip())

    def get_location(self):
        return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@id="hoteladdress"]').text.split('|')[1].strip())

    def get_price(self):
        try:
            new_price = WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//td[@class="rateamount"]').text.strip().strip('Q').strip())
            old_price = 0
            return new_price, old_price
        except:
            return 0, 0

    def get_rating(self):
        try:
            return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//img[@class="rating_circles"]').get_attribute('title'))
        except:
            return 0

    def get_review(self):
        return WebDriverWait(element, 10).until(lambda element: element.find_element_by_xpath('.//a[@class="ratingLink"]').text.strip())

def scrape_city(self, date):
    city = cities[0]
    driver = spider.chrome(url)
    close_banner(driver, banners)
    element_1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@name="city"]'))
    element_1.send_keys(city)
    element_2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('.//input[@id="checkinDate"]'))
    element_2.click()
    time.sleep(5)

    checkin = datetime.now() + timedelta(date)
    checkout = datetime.now() + timedelta(date + 3)

    while True:
        try:
            driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkin.month-1, checkin.year, checkin.day)).click()
            time.sleep(2)
            break
        except:
            driver.find_element_by_xpath('.//a[@data-handler="next"]').click()
            time.sleep(2)

    checkout_element = './/input[@id="checkoutDate"]'
    checkout_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, checkout_element)))
    checkout_element.click()
    
    while True:
        try:
            driver.find_element_by_xpath('.//td[@data-handler="selectDay"][@data-month="%s"][@data-year="%s"]/a[contains(text(), "%s")]' % (checkout.month-1, checkout.year, checkout.day)).click()
            time.sleep(2)
            break
        except:
            driver.find_element_by_xpath('.//a[@data-handler="next"]').click()
            time.sleep(2)

    search_element = './/a[contains(@title, "Go")]'
    search_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, search_element)))
    search_element.click()
    
    scrape_hotels(driver, city, checkin.strftime('%m/%d/%Y'), checkout.strftime('%m/%d/%Y'), date)
    
    driver.quit()

def scrape_hotels(driver, city, checkin, checkout, date):
    new_price, old_price = scrape_price(driver)
    name = scrape_name(driver)
    review = scrape_review(driver)
    rating = scrape_rating(driver)
    address = scrape_address(driver)
    city = city.split(',')[0]
    source = 'radisson.com'
    currency = 'GTQ'
    _db.sql_write(conn, cur, name, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, 1, date)
    print '{}, checkin {}, checkout {}, range {}, price {}'.format(source, checkin, checkout, date, new_price)
"""

if __name__ == '__main__':    
    Radisson_scraper(url)


