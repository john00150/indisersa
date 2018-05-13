from datetime import datetime
from hotels_scraper import HotelsScraper
from booking_scraper import BookingScraper
import smtplib, os
from email.mime.text import MIMEText
from settings import path, hostname


def send_email(line):
    sender = 'indisersa@radissonguat'
    recipients = [
        'yury0051@gmail.com', 
#        'oknoke@indisersa.com', 
#        'dpaz@grupoazur.com', 
#        'egonzalez@grupoazur.com'
    ]
    line = ', '.join(line) + '.'
    msg = MIMEText(line)
    msg['Subject'] = 'hotel scrapers'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


if __name__ == "__main__":
    with open(path + '/logs/launcher.log', 'w+') as fh:
        if hostname != 'john-Vostro-3558': 
            subprocess.call('taskkill /f /im chromedriver.exe')

        HotelsScraper('')
        BookingScraper('')
            
    #    send_email(fh.read())

