from subprocess import run
from sched import scheduler
from time import time
import datetime

def main():
    dates = []
    for i in range(6, 0, -1):
        dates.append((datetime.datetime.now() - datetime.timedelta(days=i)).date().day)

    results_by_date = []
    for date in dates:
        result = run(f'sar -f /var/log/sysstat/sa{date:02d}', shell=True, capture_output=True, text=True)
        lines = result.stdout.split('\n')
        hourly_results = [0.0] * 24
        for i in range(len(lines)):
            if i > 4:
                active_percent = (1.0-lines.splt(' ')[-1])
                hourly_results[(i-4)//6] += active_percent

        hourly_results = [result/6 for result in hourly_results]
    results_by_date.append(hourly_results)
    print(results_by_date)

if __name__ == "__main__":
    main()