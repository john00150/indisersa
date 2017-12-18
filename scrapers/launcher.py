from datetime import datetime
import subprocess, smtplib, os
from email.mime.text import MIMEText
from settings import log_path, scrapers, report_path


def send_email(line):
    sender = 'indisersa@radissonguat'
    recipients = ['yury0051@gmail.com'] #, 'oknoke@indisersa.com', 'dpaz@grupoazur.com', 'egonzalez@grupoazur.com']
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
    subprocess.call('taskkill /f /im chromedriver.exe')

    fh = open(log_path, 'w')

    for scraper in scrapers:
        subprocess.call(['python', scraper['path'], scraper['name']], stdout=fh)
    
