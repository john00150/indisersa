#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import re
from lxml import etree
import datetime
import codecs
import pyodbc
import time
import logging

global conn
global cur
global max_id
global checkin
global checkout

global conn
global cur
global max_id
global check_in
global check_out

def wait_until_visable(browser, element, timeout = 10):
    WebDriverWait(browser, timeout).until(
        expected_conditions.visibility_of(element))

def sql_connect(host, username, password, db):

    global conn, cur, max_id

    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=indisersa.database.windows.net;DATABASE=hotel_Info;UID=otto;PWD=Knoke@1958')
    cur = conn.cursor()

    return conn, cur

def sql_exec(conn, cur, sql):
    try:

        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print e

def sql_query(cur, sql):
    cur.execute(sql)
    return cur.fetchone()

def sql_write(conn, cur, id, hotelName, rating, review, hotelAddress,
              discountPrice, actualPrice, check_in, check_out, cityName):
    sql = "insert into tbl_hotels values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (id, hotelName, rating, review, hotelAddress, discountPrice, actualPrice, check_in, check_out, cityName)

    print sql

    sql_exec(conn, cur, sql)

def wait_until_custom(browser, method, timeout = 10):
    WebDriverWait(browser, timeout).until(method)

def get_page(browser, city):

    wait_until_custom(browser, lambda x:x.find_element_by_xpath(
            '//ol[@class="listings infinite-scroll-enabled"]/li[contains(@class, "hotel")]'), timeout=30)

    sel = etree.HTML(browser.page_source)
    items = sel.xpath('//ol[@class="listings infinite-scroll-enabled"]/li[contains(@class, "hotel")]')

    for item in items:
        hotelname = item.xpath('.//h3[@class="p-name"]/a/text()')
        if hotelname:
            hotelname = hotelname[0].strip()
        else:
            hotelname = 'Not Available'

        hotelreview = item.xpath('.//span[@class="small-view"]/text()')
        if  hotelreview:
            hotelreview = hotelreview[0]
            hotelreview = re.search('([0-9]+)', hotelreview).group(1)
        else:
            hotelreview = 'Not Available'

        hotelrating = item.xpath('.//span[@class="guest-rating-value"]/strong/text()')
        if hotelrating:
            hotelrating = hotelrating[0]
        else:
            hotelrating = 'Not Available'

        hoteladdress = item.xpath('.//p[@class="p-adr"]/span/text()')
        if hoteladdress:
            hoteladdress = ''.join(hoteladdress)
        else:
            hoteladdress = 'Not Available'

        new_price = item.xpath('.//div[@class="price"]/a/b/text()')
        old_price = 'Not Available'
        if new_price:
            new_price = new_price[0]
            old_price = new_price
        else:
            new_price = item.xpath('.//span[@class="old-price-cont"]//ins/text()')
            if new_price:
                new_price = new_price[0]
            old_price = item.xpath('.//span[@class="old-price-cont"]/del/text()')
            if old_price:
                old_price = old_price[0]

        print hotelname, hotelrating, hotelreview, hoteladdress, new_price, old_price, checkin, checkout, city
        global conn, cur, max_id
        sql_write(conn, cur, max_id, hotelname, hotelrating, hotelreview, hoteladdress, new_price, old_price, checkin, checkout, city)
        max_id += 1

    return False

def get_city(browser, city, choose_date):

    global conn, cur, max_id

    max_id = sql_query(cur, 'select max(id) from tbl_hotels')

    if max_id[0]:
        max_id = max_id[0] + 1
    else:
        max_id = 0

    start_url = 'https://www.hotels.com/?pos=HCOM_US&locale=en_US'
    browser.get(start_url)

    element = browser.find_element_by_name('q-destination')
    element.clear()
    element.send_keys(city)
    time.sleep(2)

    today = datetime.date.today()
    today_str = today.strftime('%m/%d/%Y')

    delta = datetime.timedelta(days=2)

    today_2 = today + delta
    today_2_str = today_2.strftime('%m/%d/%Y')
    today_2_str2 = today_2.strftime('%m/%d/%y')

    global checkin,checkout
    checkin = today_str
    checkout = today_2_str

    if choose_date:
        element = browser.find_element_by_xpath('//input[@name="q-localised-check-in"]')
        element.clear()
        element.send_keys(today_str)

        element = browser.find_element_by_xpath('//input[@name="q-localised-check-out"]')
        element.clear()
        element.send_keys(today_2_str)
        element.click()

        wait_until_custom(browser, lambda x:x.find_element_by_xpath('//a[@aria-label="%s"]' % today_2_str2))
        element = browser.find_element_by_xpath('//a[@aria-label="%s"]' % today_2_str2)
        element.click()

    else:                                                                              
        element = browser.find_element_by_xpath('//input[@name="q-localised-check-out"]')
        element.click()    

    element = browser.find_element_by_xpath('//button[@type="submit"]')
    element.click()

    while get_page(browser, city):
        pass

def main():
    logging.basicConfig(filename='hotels.log', level=logging.DEBUG)
    profile = webdriver.FirefoxProfile()
    profile.set_preference('webdriver.log.file', '')
    browser = webdriver.Firefox(profile)

    global conn, cur, max_id

    conn, cur = sql_connect('indisersa.database.windows.net', 'otto', 'Knoke@1958', 'hotel_Info')

    get_city(browser, 'Guatemla City, Guatemala', True)
    get_city(browser, 'Antigua Guatemala, Guatemala', False)

    conn.close()

    browser.quit()

def main_timer():
    t = time.gmtime()
    today = t.tm_yday
    today_run_once = False

    while True:
        t = time.gmtime()
        if not today_run_once:
            if t.tm_hour == 7:
                main()
                today_run_once = True
        else:
            if t.tm_yday != today:
                today = t.tm_yday
                today_run_once = False
        time.sleep(600)

if __name__ == '__main__':
    main()


