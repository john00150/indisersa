import pyodbc, time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib


def sql_exec(conn, cur, sql):
    try:
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print e

def sql_write(conn, cur, hotel, rating, review, address,new_price, old_price, checkin, checkout, city, currency, source):
    hotel = hotel.replace("'", "''")
    address = address.replace("'", "''")
    city = city.replace("'", "''")   
    sql = "insert into hotel_info (hotel_name, hotel_rating, hotel_review, hotel_address, new_price, old_price, checkin, checkout, city, currency, source) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (hotel, rating, review, address, new_price, old_price, checkin, checkout, city, currency, source)
    sql_exec(conn, cur, sql)

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

def smtp_processor():
    fromaddr = 'scrapers@indisersa.com'
    toaddrs = ['yury0051@gmail.com']
    msg = '''
        From: {fromaddr}
        To: {toaddr}
        Subject: testin'
        This is a test
        .
    '''
    msg = msg.format(fromaddr = fromaddr, toaddr = toaddrs[0])
    server = smtplib.SMTP('gmail-smtp-in.l.google.com:25')
    server.starttls()
    server.ehlo('example.com')
    server.mail(fromaddr)
    server.rcpt(toaddrs[0])
    server.data(msg)
    server.quit()


if __name__ == '__main__':
    smtp_processor()


