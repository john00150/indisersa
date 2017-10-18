from datetime import datetime
import traceback, smtplib, os
from email.mime.text import MIMEText


def send_email(line):
    sender = 'scrapers@radissonguat.com'
    recipients = ['yury0051@gmail.com', 'oknoke@indisersa.com', 'dpaz@grupoazur.com', 'egonzalez@grupoazur.com']
    line = ', '.join(line) + '.'
    msg = MIMEText(line)
    msg['Subject'] = 'hotel scrapers'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

if __name__ == '__main__':
    try:
        os.system('taskkill /f /im chromedriver.exe')
    except:
        try:
            os.system('taskkil /f /im geckodriver.exe')
        except:
            pass
    
    fh = open('C:\users\indisersa\Desktop\hotels\logs\launcher.log', 'w')
    fh.write('start: %s\n' % datetime.now())
    line = list()

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\marriott_scraper.py')
    except Exception, e:
        fh.write('marriott_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('marriott_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\radisson_scraper.py')
    except Exception, e:
        fh.write('radisson_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('radisson_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\lodebernal_scraper.py')
    except Exception, e:
        fh.write('lodebernal_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('lodebernal_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\bestday_scraper.py')
    except Exception, e:
        fh.write('bestday_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('bestday_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\despegar_scraper.py')
    except Exception, e:
        fh.write('despegar_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('despegar_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\elconventoantigua_scraper.py')
    except Exception, e:
        fh.write('elconventoantigua_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('elconventoantigua_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\expedia_scraper.py')
    except Exception, e:
        fh.write('expedia_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('expedia_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\book_hotel_beds_scraper.py')
    except Exception, e:
        fh.write('book_hotel_beds_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('book_hotel_beds_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\hotels_scraper.py')
    except Exception, e:
        fh.write('hotels_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('hotels_scraper error')
        print e
    print '#' * 50

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\booking_scraper.py')
    except Exception, e:
        fh.write('booking_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line.append('booking_scraper error')
        print e
    print '#' * 50

    fh.write('finish: %s' % datetime.now())

    if len(line) > 0:
        send_email(line)

    fh.close()


    
    
