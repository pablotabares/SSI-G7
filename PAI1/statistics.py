import os
import datetime


def stats(log_name):
    now = datetime.datetime.now()
    s = now.strftime('%Y-%m-%d')

    kpi_name = 'kpi_' + log_name
    trend = ''
    comp = None

    with open(log_name, "r") as f:
        pos = 0
        neg = 0
        for line in enumerate(f):
            if ('[CRITICAL]' in str(line)):
                neg += 1
            elif ('[ERROR]' in str(line)):
                neg += 1
            elif ('[WARNING]' in str(line)):
                neg += 1
            elif ('[INFO]' in str(line)):
                pos += 1
            elif ('[DEBUG]' in str(line)):
                pos += 1

    daily_ratio = pos/(pos+neg)

    try:
        with open(kpi_name, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
    except:
        last_line = None

    if last_line is not None:
        prev_ratio = float(last_line[1:4])
        comp = round(daily_ratio,2) >= prev_ratio
        trend = ' Possitive trend' if comp else ' Negative trend'

    file = open(kpi_name, "a")
    file.write('{0:.2f}'.format(daily_ratio) + trend + "\n")
    file.close()

    return (daily_ratio, comp)

stats("log_2019_3.log")
