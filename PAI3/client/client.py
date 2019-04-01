#!/usr/bin/env python3
import hashlib
import hmac
import json
import sys
import os
from datetime import datetime
import bcrypt
import base64
import socket_client
import sqlite3
import julian

def send():
    num = input('Origin Account:')
    acc = fetch_account(num)
    if acc is None:
        confirm = input('Account not set up. Would you like to set it up?[Y/N]')
        if confirm not in ['Y','y','yes']:
            print('Exiting...')
            exit()
        new_key(src)
        acc = fetch_account(num)
    dst = input('Destination Account Nº:')
    amt = 0
    while amt <= 0.00:
        amt = float(input('Amount to transfer in €:'))
    msg = num+'|$|'+dst+'|$|'+str(amt)+'|$|'+str(julian.to_jd(datetime.now()))
    print(msg)
    digest = hmac.new(bytes(acc[1],'utf-8'), bytes(msg,'utf-8'), 'sha256').hexdigest()
    print(digest)
    socket_client.connect_and_send(msg+'|$|'+digest)


def new_key(src=None,key=None):
    mode = 'added'
    src = input('Account Nº to set-up:') if src is None else src
    if fetch_account(src) is not None:
        mode = 'updated'
        over = input('Account already exists, are you sure you want to overwrite its key? [Y/N]')
        if over not in ['Y','y','yes']:
            print('Exiting...')
            exit()
    key = input('Please introduce the HMAC key:') if key is None else key
    store_account(src, key)
    print('Account '+ mode + ' successfully!')
    return

def print_accounts():
    for acc in fetch_accounts():
        print(acc[0]+': ' + acc[1])
    return

def check_db(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name in ('keys')")
    return len(c.fetchall()) >= 1

def initialize_db():
    [conn, c] = get_connection()
    if check_db(c):
        conn.close()
        print('Database already initialized')
        return
    c.execute('''CREATE TABLE keys (account, key)''')
    conn.commit()
    conn.close()
    print('Database initialized')
    return

def get_connection():
    conn = sqlite3.connect('mykeys.db')
    return [conn, conn.cursor()]

def fetch_accounts():
    [conn, c] = get_connection()
    c.execute('SELECT * FROM keys')
    keys = c.fetchall()
    conn.close()
    return keys

def fetch_account(acc):
    [conn, c] = get_connection()
    params = (acc,)
    c.execute('SELECT * FROM keys where account = ?',params)
    account = c.fetchone()
    conn.close()
    return account

def store_account(src, key):
    acc = fetch_account(src)
    [conn, c] = get_connection()
    if(acc is None):
        params = (src, key)
        c.execute("INSERT INTO keys(account, key) VALUES (?,?)", params)
    else:
        params = (key, src)
        c.execute('UPDATE keys SET key = ? WHERE account = ?', params)
    conn.commit()
    conn.close()
    return

# try:
if len(sys.argv) < 2:
    print('-- INSEGUS GROUP 7 BANK CLIENT --')
    print('Re-run the script with one of the following options')
    print('->send (To make a transaction)')
    print('->new <account> <key> (To add a new account to the system)')
    print('->import (To import a new account to the system with its key)')
    print('->install (To install the system)')
    print('->list (To list your accounts)')
else:
    function = sys.argv[1]
    if function == 'send':
        send()
    elif function == 'new':
        new_key()
    elif function == 'import':
        new_key(src, key)
    elif function == 'install':
        initialize_db()
    elif function == 'list':
        print_accounts()
    else:
        print('That action does not exist')
# except Exception as ex:
#     msg = 'Exception of type {0} occurred: {1}'.format(type(ex).__name__, ex.args[0])
#     logger(msg=msg, type='CRITICAL')
