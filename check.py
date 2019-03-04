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

def find_hash(filename):
    f = open('hashes.txt','r')
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
        f = open('hashes.txt','a')
        f.write(filename + cfg.hashes_divider + base64.b64encode(hashed).decode('utf-8') + "\n")
    except FileNotFoundError:
        error('FILE NOT FOUND', filename)


def check(filename):
    try:
        open(filename,'r').close() #nos aseguramos que existe el archivo
        hash = find_hash(filename)
        if hash is None:
            generate(filename)
            info('HASH GENERATED')
            return
        blakehash = get_blake2b_file(filename)
        check = bcrypt.checkpw(blakehash, base64.b64decode(hash))
        if check:
            info('SUCCESSFUL', filename)
        else:
            error('INTEGRITY FAIL', filename)
        return check
    except FileNotFoundError:
        error('FILE NOT FOUND', filename)

def reset():
    f = open('hashes.txt','w').close()

def login(user, password):
    # Tries to authenticate a user.
    # Returns True if the authentication succeeds, else the reason
    # (string) is returned.
    try:
        enc_pwd = spwd.getspnam(user)[1]
        if enc_pwd in ["NP", "!", "", None]:
            return "user '%s' has no password set" % user
        if enc_pwd in ["LK", "*"]:
            return "account is locked"
        if enc_pwd == "!!":
            return "password has expired"
        # Encryption happens here, the hash is stripped from the
        # enc_pwd and the algorithm id and salt are used to encrypt
        # the password.
        if crypt.crypt(password, enc_pwd) == enc_pwd:
            return True
        else:
            return "incorrect password"
    except KeyError:
        return "user '%s' not found" % user
    return "unknown error"

def config_has_changed():
    is_ok = check(filename='config.py')
    if not is_ok:
        error('CONFIGURATION FILE HAS CHANGED, WANT TO RESET? [Y,N]')
        confirm = input('CONFIGURATION FILE HAS CHANGED, WANT TO RESET? [Y,N]')
        if confirm in ['Y','yes','y']:
            admin_user = input('Admin User:')
            admin_pass = getpass('Password:')
            login_result = login(admin_user, admin_pass)
            if login_result is True:
                info('RESETING...')
                reset()
                generate('config.py')
                for file in cfg.files:
                    generate(file)
                return True
            else:
                error(login_result)
                return False
        else:
            print('EXITING...')
            return False
    else:
        return True

def logger(msg, type, filename=None):
    if cfg.log_levels.get(type) >= cfg.log_level:
        filetext = ' FILE: ' + filename + ' //' if filename is not None else ''
        log_msg = datetime.datetime.now().strftime('%d-%b-%y %H:%M:%S') + \
          '[' + type + '] =>' + filetext + ' MSG: ' + msg
        if 'terminal' in cfg.log_types:
            print(log_msg)
        if 'file' in cfg.log_types:
            logname = cfg.log_file if hasattr(cfg,'log_file') else 'log.log'
            f = open(logname,'a')
            f.write(log_msg + "\n")

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
        print('Please specify an action')
    else:
        function = sys.argv[1]
        if function == 'check':
            if config_has_changed() is True:
                for file in cfg.files:
                    check(file)
        elif function == 'reset':
            reset()
        else:
            print('That action does not exist')
except Exception as ex:
    msg = 'Exception of type {0} occurred: {1}'.format(type(ex).__name__, ex.args[0])
    logger(msg=msg, type='CRITICAL')
