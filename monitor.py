import datetime
import smtplib
import ssl
from os import environ
from sched import scheduler
from subprocess import run
from time import time

ssl_port = 465

message = """\
Subject: Your Raspberry Pi

{}
"""

def get_cpu_stats(date):
    result = run(f'sar -f /var/log/sysstat/sa{date:02d}', shell=True, capture_output=True, text=True)
    lines = result.stdout.split('\n')
    lines = lines[5:-1] #Cut out the header and footer lines
    hourly_results = [0.0] * 24
    for i in range(len(lines)):
        active_percent = 100.0-float(lines[i].split(' ')[-1])
        hourly_results[i//6] += active_percent

    return [result/6 for result in hourly_results]

def main():
    dates = []
    for i in range(6, -1, -1):
        dates.append((datetime.datetime.now() - datetime.timedelta(days=i)).date().day)

    cpu_results = []
    for date in dates:
        cpu_results.append(get_cpu_stats(date))

    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=ssl.create_default_context()) as server:
        server.login(environ.get('SOURCE_EMAIL'), environ.get('SOURCE_PASSWORD'))
        server.sendmail(environ.get('SOURCE_EMAIL'), environ.get('DESTINATION_EMAIL'), message.format(cpu_results))
    print(cpu_results)

if __name__ == "__main__":
    main()
