import pyodbc, time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime


def sql_exec(conn, cur, sql):
    try:
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print e

def sql_write(conn, cur, hotel, rating, review, address,new_price, old_price, checkin, checkout, city, currency, source, count):
    hotel = hotel.replace("'", "''")
    address = address.replace("'", "''")
    city = city.replace("'", "''")
    sql = "insert into hotel_info (hotel_name, hotel_rating, hotel_review, hotel_address, new_price, old_price, checkin, checkout, city, currency, source, date_scraped, hotel_position) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source, datetime.now().strftime('%m/%d/%Y'), count)
    try:
        sql_exec(conn, cur, sql)
    except:
        pass

def spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(800, 600)
    driver.get(url)
    return driver

def csv_write(fh, name, review, rating, address, currency, new_price, old_price, checkin, checkout, city, source):
        line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, review, rating, address, currency, new_price, old_price, checkin, checkout, city, source)
        fh.write(line.encode('utf8'))


