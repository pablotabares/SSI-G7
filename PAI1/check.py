#!/usr/bin/env python3
import bcrypt
from hashlib import blake2b
import base64
import sys
import config as cfg
import datetime
import crypt
from getpass import getpass
import spwd
from logger import logger
import os
import subprocess
from crontab import CronTab

def find_hash(filename):
    f = open(cfg.project_path+'hashes.txt','r')
    hash = None
    for line in f:
        if filename in line:
            hash = line.split(cfg.hashes_divider)[1]
    return hash

def bytes_from_file(filename, chunksize=cfg.chunksize):
    with open(filename,'rb') as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
            else:
                break

def get_blake2b_file(filename):
    m = blake2b(digest_size=16)
    m.update(bytes(filename,'utf-8'))
    salt = m.digest()
    m = blake2b(salt=salt)
    for chunk in bytes_from_file(filename):
        m.update(chunk)
    return base64.b64encode(m.digest())

def generate(filename):
    try:
        blakehash = get_blake2b_file(filename)
        hashed = bcrypt.hashpw(
            blakehash,
            bcrypt.gensalt(10)
        )
        f = open(cfg.project_path+'hashes.txt','a')
        f.write(filename + cfg.hashes_divider + base64.b64encode(hashed).decode('utf-8') + "\n")
    except FileNotFoundError:
        error('FILE NOT FOUND', filename)


def check(filename):
    try:
        open(filename,'r').close() #nos aseguramos que existe el archivo
    except FileNotFoundError:
        error('FILE NOT FOUND', filename)
        return False
    hash = find_hash(filename)
    if hash is None:
        generate(filename)
        info('HASH GENERATED')
        return False
    blakehash = get_blake2b_file(filename)
    check = bcrypt.checkpw(blakehash, base64.b64decode(hash))
    if check:
        info('SUCCESSFUL', filename)
    else:
        error('INTEGRITY FAIL', filename)
    return check

def reset():
    if os.geteuid() == 0:
        f = open(cfg.project_path+'hashes.txt','w').close()
        generate(cfg.project_path+'config.py')
        for file in cfg.files:
            generate(file)
        add_to_cron()
        return True
    else:
        error('You need root privileges to reset')
        return False

def config_has_changed():
    is_ok = check(filename=cfg.project_path+'config.py')
    if not is_ok:
        error('Configuration file has changed. Please re-run this script with the reset option.')
    else:
        return True

def install():
    info('INSTALLING...')
    reset()
    info('¡¡INSTALLATION COMPLETE. HIDS CHECK WILL RUN EVERY ' + str(cfg.cron_time) + ' MINUTES!!')

def add_to_cron():
    crontab = CronTab(user='root')
    for job in crontab:
        if job.comment == 'hidscheck':
            crontab.remove(job)
    job = crontab.new(command=cfg.project_path+'check.py check', comment='hidscheck')
    job.minute.every(cfg.cron_time)
    crontab.write()
    info('Cron entry updated')

def info(msg, filename=None):
    logger(msg, 'INFO', filename)

def error(msg, filename=None):
    logger(msg, 'ERROR', filename)

def debug(msg, filename=None):
    logger(msg, 'DEBUG', filename)

def warn(msg, filename=None):
    logger(msg, 'WARN', filename)

try:
    if len(sys.argv) < 2:
        print('-- INSEGUS GRUPO 7 HIDS --')
        print('Re-run the script with one of the following options')
        print('+check:')
        print('\t Hash checking')
        print('+reset:')
        print('\t Reset after config changes are applied')
        print('+install:')
        print('\t First set-up command')
    else:
        function = sys.argv[1]
        if function == 'check':
            if config_has_changed() is True:
                for file in cfg.files:
                    check(file)
        elif function == 'reset':
            reset()
        elif function == 'install':
            install()
        else:
            print('That action does not exist')
except Exception as ex:
    msg = 'Exception of type {0} occurred: {1}'.format(type(ex).__name__, ex.args[0])
    logger(msg=msg, type='CRITICAL')
