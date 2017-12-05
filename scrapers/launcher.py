from datetime import datetime
import traceback, smtplib, os
from email.mime.text import MIMEText
from settings import log_path, scrapers


def send_email(line):
    sender = 'indisersa@radissonguat'
    recipients = ['yury0051@gmail.com', 'oknoke@indisersa.com', 'dpaz@grupoazur.com', 'egonzalez@grupoazur.com']
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
    try:
        os.system('taskkill /f /im chromedriver.exe')
    except:
        pass
    
    l = list()

    fh_report = open(report_path, 'w')
    fh_log = open(log_path, 'w')
    fh_log.write('start: %s\n' % datetime.now())

    for scraper in scrapers:
        try:
            execfile(scraper['path'])

        except Exception, e:
            name = scraper['name']
            message_line = "{} error".format(name)
            l.append(message_line)
            
            print traceback.print_exc()
            fh_log.write('########## {} ##########\n'.format(name))
            traceback.print_exc(file=fh_log)
            fh_log.write('\n#######################\n')

    fh_log.write('finish: %s\n' % datetime.now())
    fh_log.close()
    fh_report.close()

    if len(l) > 0:
        send_email(l)


    
    
