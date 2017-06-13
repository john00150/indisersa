import pyodbc
from selenium import webdriver

def sql_connect(host, username, passwd, db):
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client #11.0};SERVER=indisersa.database.windows.net;DATABASE=hotel_Info;UID=otto;PWD=Knoke@1958')
    cur = conn.cursor()
    return conn, cur

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
    #driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    driver.set_window_size(800, 600)
    driver.get(url)
    time.sleep(5)
    return driver

