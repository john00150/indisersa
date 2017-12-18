from datetime import datetime
import subprocess, smtplib, os
from email.mime.text import MIMEText
from settings import log_path, scrapers, report_path


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
    l = list()

#    fh_report = open(report_path, 'w')
    fh = open(log_path, 'w')
#    fh.write('start: {}\n\n'.format(datetime.now().strftime('%Y-%m-%d')))
    subprocess.call('taskkill /f /im chromedriver.exe')

    for scraper in scrapers:
        subprocess.call(['python', scraper['path']], stderr=fh)
            #s.communicate()

#        try:
#            execfile(scraper['path'])

#        except Exception, e:
#            name = scraper['name']
#            message_line = "{} error".format(name)
#            l.append(message_line)
            
#            print traceback.print_exc()
#            fh_log.write('########## {} ##########\n'.format(name))
#            traceback.print_exc(file=fh_log)

#    fh.write('finish: {}'.format(datetime.now().strftime('%Y-%m-%d')))
    fh.close()

#    if len(l) > 0:
#        send_email(l)


    
    
