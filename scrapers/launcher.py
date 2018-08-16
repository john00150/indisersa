from __future__ import print_function
from datetime import datetime
from banguat_scraper import BanguatScraper 
from hotels_scraper import HotelsScraper
from booking_scraper import BookingScraper
from despegar_scraper import DespegarScraper
from radisson_scraper import RadissonScraper
from elconventoantigua_scraper import ElconventoantiguaScraper
from lodebernal_scraper import LodebernalScraper
from marriott_scraper import MarriottScraper
from expedia_scraper import ExpediaScraper
from bestday_scraper import BestDayScraper
from book_hotel_beds_scraper import BookHotelBedsScraper
import smtplib, os, subprocess
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
        try: BanguatScraper(None)
        except Exception as e: print(e)

        try: HotelsScraper('')
        except Exception as e: print(e)
        
        try: BookingScraper('')
        except Exception as e: print(e)
        
        try: DespegarScraper('')
        except Exception as e: print(e)
        
        try: RadissonScraper(None)
        except Exception as e: print(e)
        
        try: ElconventoantiguaScraper('')
        except Exception as e: print(e)
        
        try: LodebernalScraper('')
        except Exception as e: print(e)
        
        try: MarriottScraper('')
        except Exception as e: print(e)
        
        try: ExpediaScraper('')
        except Exception as e: print(e)
        
        try: BestDayScraper('')
        except Exception as e: print(e)
        
        try: BookHotelBedsScraper('')
        except Exception as e: print(e)
            
    #    send_email(fh.read())

