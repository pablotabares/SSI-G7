import os
import datetime


def logger(msg, type, file_name):

    now = datetime.datetime.now()
    log_name = 'log_' + str(now.year) + '_' + str(now.month) + '.log'
    prev_log_name = 'log_' + str(now.year) + '_' + str(now.month-1) + '.log'

    exits = os.path.isfile('./' + log_name) 
    filetext = ' FILE: ' + file_name + ' //' if file_name is not None else ''

    if(now.day == 1 and not exits) :
        rename(prev_log_name)

    file = open(log_name, 'a')
    file.write('[' + type + '] ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' => ' + filetext + ' MSG: ' + msg + '\n')
    file.close()

    neg_verified = ['WARNING', 'ERROR', 'CRITICAL']

    if(type in neg_verified):
        report_name = 'report_' + str(now.year) + '_' + str(now.month) + '.log'
        f = open(report_name, 'a')
        f.write(file_name + ',')

def rename(file_name):
    pre, ext = os.path.splitext(file_name)
    os.rename(file_name, pre + '.bak')


logger("mensaje" , "WARNING", "Archivo.txt")
