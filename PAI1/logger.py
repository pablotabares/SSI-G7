import os
import datetime
import config as cfg

def logger(msg, type, file_name=None):
    if cfg.log_levels[type] < cfg.log_level:
        return
    now = datetime.datetime.now()
    log_name = 'log_' + str(now.year) + '_' + str(now.month) + '.log'
    prev_log_name = 'log_' + str(now.year) + '_' + str(now.month-1) + '.log'

    exits = os.path.isfile(cfg.project_path + log_name)
    filetext = ' FILE: ' + file_name + ' //' if file_name is not None else ''

    if(now.day == 1 and not exits) :
        rename(prev_log_name)

    log_msg = '[' + type + '] ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' => ' + filetext + ' MSG: ' + msg
    if 'terminal' in cfg.log_types:
        print(log_msg)
    if 'file' in cfg.log_types:
        f = open(cfg.project_path + log_name,'a')
        f.write(log_msg + "\n")
        f.close()

    neg_verified = ['WARNING', 'ERROR', 'CRITICAL']

    if(type in neg_verified and file_name is not None):
        report_name = 'report_' + str(now.year) + '_' + str(now.month) + '.log'
        f = open(report_name, 'a')
        f.write(file_name + ',')

def rename(file_name):
    pre, ext = os.path.splitext(file_name)
    os.rename(file_name, pre + '.bak')
