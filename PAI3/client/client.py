#!/usr/bin/env python3
import hashlib
import hmac
import json
import sys
import os
from datetime import datetime
import bcrypt
import base64
import sqlite3
import julian
import socket
import ssl

def connect_and_send():
    # Se establece la conexion
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(sock)
    conn.connect(("localhost", 443))

    # Recibimos la petición de correo y lo enviamos
    rec = conn.recv(1000)
    mail = input(rec.decode())
    conn.send(mail.encode())

    #Recibimos la petición de contraseña y la enviamos
    rec = conn.recv(1000)
    pwd = input(rec.decode())
    conn.send(pwd.encode())

    #Recibimos la resupuesta del login y la imprimimos en pantalla
    login_result = conn.recv(1000).decode()
    login_msg = conn.recv(1000).decode()
    print('[SERVER] ' + login_msg)

    if login_result != 'true':
        conn.close()
        return

    #Generamos y enviamos la transferencia
    msg = send()
    conn.send(msg.encode())

    # Se recibe la respuesta y se escribe en pantalla
    datos = conn.recv(1000)
    print('[SERVER] ' + datos.decode())
    conn.close()

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
    digest = hmac.new(bytes(acc[1],'utf-8'), bytes(msg,'utf-8'), 'sha256').hexdigest()
    return msg+'|$|'+digest


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
        connect_and_send()
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
