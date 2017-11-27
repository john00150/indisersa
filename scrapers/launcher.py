from datetime import datetime
import traceback, smtplib, os
from email.mime.text import MIMEText
from settings import log_path, scrapers


def send_email(line):
    sender = 'scrapers@radissonguat.com'
    recipients = ['yury0051@gmail.com']#, 'oknoke@indisersa.com', 'dpaz@grupoazur.com', 'egonzalez@grupoazur.com']
    line = ', '.join(line) + '.'
    msg = MIMEText(line)
    msg['Subject'] = 'hotel scrapers'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

def run_scraper(scraper_path, l, fh):
    name = ''
    message_line = "{} error".format(name)

    try:
        execfile(scraper_path)
    except Exception, e:
        print traceback.print_exc()
        traceback.print_exc(file=fh)
        fh.write('\n\n')
        l.append(message_line)


if __name__ == "__main__":    
#    try:
#        os.system('taskkill /f /im chromedriver.exe')
#    except:
#        pass

    
    fh = open(log_path, 'w')
    fh.write('start: %s\n' % datetime.now())
    l = list()

    for scraper in scrapers:
        try:
            execfile(scraper['path'])
            
        except Exception, e:
            name = scraper['name']
            message_line = "{} error".format(name)
            l.append(message_line)
            
            print traceback.print_exc()
            traceback.print_exc(file=fh)
            fh.write('\n\n')

    if len(l) > 0:
        send_email(l)


    
    
