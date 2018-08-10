from __future__ import print_function
import requests, time, traceback, sys
from base_scraper import BaseScraper
from lxml import html
from datetime import datetime

class BanguatScraper(BaseScraper):
    def __init__(self, mode):
        self.mode = mode
        self.log_path = 'C:\\users\\indisersa\\Desktop\hotels\\logs\\banguat.log'
        self.url = 'http://banguat.gob.gt/default.asp'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
        }
        BaseScraper.__init__(self)

    def main_function(self):
        try:
            self.get_rate()
        except Exception:
            traceback.print_exc()

    def get_rate(self):
        r = requests.get(
            self.url,
            headers = self.headers,
        )

        tree = html.fromstring(r.content)
        
        element = tree.xpath(
            './/tr[@class="txt-resumen"]/td[./strong/a[contains(@href, "cambio/default.asp")]]/following-sibling::td/text()'
        )
        element = element[0].strip()

        if self.mode == 'print': 
            print(element)

        query = "INSERT INTO banguat (date_scraped, banguate_rate) values ('%s', '%s')" % (
            self.current_date, element
        )

        if self.hostname != 'john-Vostro-3558':
            self.cur.execute(query)
            self.conn.commit()

if __name__ == "__main__":
    try: 
        mode = sys.argv[1]
    except:
        mode = None

    BanguatScraper(mode)
    
