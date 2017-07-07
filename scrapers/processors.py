import pyodbc, time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def sql_exec(conn, cur, sql):
    try:
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print e

def sql_write(conn, cur, hotel, rating, review, address,new_price, old_price, checkin, checkout, city):
    sql = "insert into tbl_hotels values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (hotel, rating, review, address, new_price, old_price, checkin, checkout, city)
    sql_exec(conn, cur, sql)

def spider(url):
    #proxy = '159.203.117.131:3128'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    #chrome_options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(800, 600)
    driver.get(url)
    time.sleep(5)
    return driver

def csv_open(fn):
    fh = open('output/%s.csv' % fn, 'w')
    header = 'name,review,rating,address,currency,new_price,old_price,checkin,checkout,city\n'
    fh.write(header)
    return fh

def csv_write(fh, name, review, rating, address, currency, new_price, old_price, checkin, checkout, city):
        line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, review, rating, address, currency, new_price, old_price, checkin, checkout, city)
        fh.write(line.encode('utf8'))

def checkin_checkout(index):
    if index == 0:
        checkin = datetime.date.today()
        checkin = checkin.strftime('%m/%d/%Y')

        delta = datetime.timedelta(days=2)
        checkout = datetime.date.today() + delta
        checkout_1 = checkout.strftime('%m/%d/%Y')
        checkout_2 = checkout.strftime('%m/%d/%y')

    if index == 1:
        delta_1 = datetime.timedelta(days=120)
        checkin = datetime.date.today() + delta_1
        checkin = checkin.strftime('%m/%d/%Y')

        delta_2 = datetime.timedelta(days=122)
        checkout = datetime.date.today() + delta_2
        checkout_1 = checkout.strftime('%m/%d/%Y')
        checkout_2 = checkout.strftime('%m/%d/%y')

    return checkin, checkout_1, checkout_2


