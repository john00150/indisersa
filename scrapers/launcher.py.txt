from datetime import datetime


if __name__ == '__main__':
    fh = open('C:\users\indisersa\Desktop\hotels\logs\launcher.log', 'a')
    fh.write('start: %s\n' % datetime.now())
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\marriott_scraper.py')
    except:
        fh.write('marriott_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\radisson_scraper.py')
    except:
        fh.write('radisson_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\bestday_scraper.py')
    except:
        fh.write('bestday_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\booking_scraper.py')
    except:
        fh.write('booking_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\despegar_scraper.py')
    except:
        fh.write('despegar_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\elconventoantigua_scraper.py')
    except:
        fh.write('elconventoantigua_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\expedia_scraper.py')
    except:
        fh.write('expedia_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\book_hotel_beds_scraper.py')
    except:
        fh.write('book_hotel_beds_scraper failed')
    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\hotels_scraper.py')
    except:
        fh.write('hotels_scraper failed')
    fh.write('finish: %s\n' % datetime.now())
