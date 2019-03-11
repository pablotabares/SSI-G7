#!/usr/bin/env python3
import hashlib
import hmac
import json
import sys
import os

def send():
    dst = input('Destination Account Nº:')
    amt = input('Amount to transfer in €:')


def new_key():
    f = open('keys.json')
    accounts = json.load(f)
    f.close()
    src = input('Account Nº to set-up:')
    if src in accounts:
        over = input('Account already exists, are you sure you want to overwrite its key? [Y/N]')
        if over not in ['Y','y','yes']:
            print('Exiting...')
            exit()
    key = input('Please introduce your HMAC key:')
    accounts[src] = key
    f2 = open('keys.json','w')
    json.dump(accounts, f2)
    f2.close()

# try:
if len(sys.argv) < 2:
    print('-- INSEGUS GRUPO 7 BANK CLIENT --')
    print('Re-run the script with one of the following options')
else:
    function = sys.argv[1]
    if function == 'send':
        send()
    elif function == 'new':
        new_key()
    else:
        print('That action does not exist')
# except Exception as ex:
#     msg = 'Exception of type {0} occurred: {1}'.format(type(ex).__name__, ex.args[0])
#     logger(msg=msg, type='CRITICAL')
