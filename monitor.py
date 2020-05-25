import datetime
import smtplib
import ssl
from email.message import EmailMessage
from io import BytesIO
from os import environ
from subprocess import run
from time import sleep

import schedule
from matplotlib import pyplot

ssl_port = 465


def trim_lines(lines):
    lines = lines[1:]
    useful_lines = []
    for line in lines:
        if not 'LINUX RESTART' in line and not '%' in line and not line.strip() == '' and not 'Average:' in line:
            useful_lines.append(line)
    return useful_lines

def get_cpu_stats(date):
    result = run(f'sar -f /var/log/sysstat/sa{date:02d}', shell=True, capture_output=True, text=True)
    lines = trim_lines(result.stdout.split('\n'))
    hourly_results = [0.0] * 24
    for i in range(len(lines)):
        active_percent = 100.0-float(lines[i].split(' ')[-1])
        hourly_results[i//6] += active_percent

    return [result/6 for result in hourly_results]

def send_statistics():
    dates = []
    for i in range(6, -1, -1):
        dates.append((datetime.datetime.now() - datetime.timedelta(days=i)))

    hourly_dates = []
    for i in range(len(dates)*24):
        hourly_dates.append(dates[0] + datetime.timedelta(hours=i))

    dates = [date.date().day for date in dates]

    cpu_results = []
    for date in dates:
        cpu_results.extend(get_cpu_stats(date))

    image = BytesIO()
    pyplot.figure(figsize=(20,10))
    pyplot.ylim(0, 100)
    pyplot.plot(hourly_dates, cpu_results)
    pyplot.savefig(image, format='jpg')
    image.seek(0)

    message = EmailMessage()
    message['Subject'] = 'Your Raspberry Pi'
    message.add_attachment(image.read(), maintype='application', subtype='octet-stream', filename='cpu.jpg')

    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=ssl.create_default_context()) as server:
        server.login(environ.get('SOURCE_EMAIL'), environ.get('SOURCE_PASSWORD'))
        server.send_message(message, environ.get('SOURCE_EMAIL'), environ.get('DESTINATION_EMAIL'))


def go():
    print('ran')

def main():
    schedule.every(1).minutes.do(go)

    while True:
        schedule.run_pending()
        sleep(60)


if __name__ == "__main__":
    main()
