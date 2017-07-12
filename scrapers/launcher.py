from datetime import datetime
import traceback


if __name__ == '__main__':
    fh = open('C:\users\indisersa\Desktop\hotels\logs\launcher.log', 'a')
    fh.write('start: %s\n' % datetime.now())

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\marriott_scraper.py')
    except Exception:
        fh.write('marriott_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\radisson_scraper.py')
    except Exception:
        fh.write('radisson_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\bestday_scraper.py')
    except Exception:
        fh.write('bestday_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\booking_scraper.py')
    except Exception:
        fh.write('booking_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\despegar_scraper.py')
    except Exception:
        fh.write('despegar_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\elconventoantigua_scraper.py')
    except Exception:
        fh.write('elconventoantigua_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\expedia_scraper.py')
    except Exception:
        fh.write('expedia_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\book_hotel_beds_scraper.py')
    except Exception:
        fh.write('book_hotel_beds_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\hotels_scraper.py')
    except Exception:
        fh.write('hotels_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')

    fh.write('finish: %s\n' % datetime.now())
    fh.write('#'*50+'\n')

