from datetime import datetime
import traceback, smtplib, os
from email.mime.text import MIMEText


def send_email(line):
    sender = 'scrapers@radissonguat.com'
    recipients = ['yury0051@gmail.com', 'oknoke@indisersa.com', 'dpaz@grupoazur.com', 'egonzalez@grupoazur.com']
    msg = MIMEText(line)
    msg['Subject'] = 'hotel scrapers'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

if __name__ == '__main__':
    os.system('taskkill /f /im chromedriver.exe')
    fh = open('C:\users\indisersa\Desktop\hotels\logs\launcher.log', 'w')
    fh.write('start: %s\n' % datetime.now())
    line = ''

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\hotels_scraper.py')
    except Exception:
        fh.write('hotels_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'hotels_scraper error ' 

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\marriott_scraper.py')
    except Exception:
        fh.write('marriott_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'marriott_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\radisson_scraper.py')
    except Exception:
        fh.write('radisson_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'radisson_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\bestday_scraper.py')
    except Exception:
        fh.write('bestday_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'bestday_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\booking_scraper.py')
    except Exception:
        fh.write('booking_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'booking_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\despegar_scraper.py')
    except Exception:
        fh.write('despegar_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'despegar_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\elconventoantigua_scraper.py')
    except Exception:
        fh.write('elconventoantigua_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'elconventoantigua_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\expedia_scraper.py')
    except Exception:
        fh.write('expedia_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'expedia_scraper error '

    try:
        execfile('C:\users\indisersa\Desktop\hotels\scrapers\\book_hotel_beds_scraper.py')
    except Exception:
        fh.write('book_hotel_beds_scraper failed\n')
        traceback.print_exc(file=fh)
        fh.write('\n')
        line += 'book_hotel_beds_scraper error '

    fh.write('finish: %s' % datetime.now())
    fh.close()

    if len(line) > 0:
        send_email(line)


    
    
