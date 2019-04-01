import os
import datetime
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def plot():

    now = datetime.datetime.now()
    kpi_name = 'kpi_' + 'log_' + str(now.year) + '_' + str(now.month-1) + '.log'
    report_name = 'report_' + str(now.year) + '_' + str(now.month-1) + '.log'
    chart_name = 'line_chart_' + str(now.year) + '_' + str(now.month-1) + '.png'

    with open(kpi_name, 'r') as f:
        points = {}
        count = 1
        for line in enumerate(f):
            ratio = line[1]
            n_ratio = ratio[0:4]
            points[count] = float(n_ratio)
            count += 1

    plt.plot(list(points.keys()), list(points.values()), 'bo')
    plt.plot([0, count],[0.95, 0.95], 'r')
    plt.axis([0, count, 0, 1.05])
    plt.title('Daily integrity ratio and threshold line')
    plt.xlabel('Day of the month')
    plt.ylabel('Ratios')
    plt.savefig(chart_name, dpi = 200)

    with open(report_name, 'a') as r:
        r.write('\n' + '\n' + 'Day/ratio pairs of the month: ' + str(points) + '\n' +
            'The line chart has been generated with the name' + chart_name)

plot()
