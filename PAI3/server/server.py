import hashlib
import hmac
import json
import sys
import os
from datetime import datetime
import bcrypt
import base64
import sqlite3
from sendMail import sendMail
from texttable import Texttable
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def add_client(src=None):
    mode = 'added'
    owner = input('Account Owner Email:')
    src = input('Account Nº to set-up:')
    if fetch_account(src) is not None:
        mode = 'updated'
        over = input('Account already exists, are you sure you want to overwrite its key and password? [Y/N]')
        if over not in ['Y','y','yes']:
            print('Exiting...')
            exit()
    key = input('Please introduce the HMAC key:')
    pwd = input('Please introduce the new password:')
    store_account(src, key, owner, pwd)
    sendMail(owner,'Welcome to Group7 Bank','Your account with number ' + src + ' has been set up with key ' + key + '. You may import your account by typing: client.py import ' + src + ' ' + key)
    print('Account '+ mode + ' successfully!')
    return

def receive(msg, logged_acc):
    [src, dst, amt, time, rec_digest] = msg.split('|$|')
    acc = fetch_account(src)
    if acc is None:
        return [-1, 'Non existing account']
    if acc[0] != logged_acc[0]:
        return [-1, 'This account is not owned by the logged in user']
    check_msg = '|$|'.join(str(x) for x in [src, dst, amt, time])
    gen_digest = hmac.new(bytes(acc[1],'utf-8'), bytes(check_msg,'utf-8'), 'sha256').hexdigest()
    if (not hmac.compare_digest(rec_digest, gen_digest)):
        store_transaction(src, dst, float(amt), float(time), 1)
        return [-1, 'Non matching digests']
    elif fetch_transaction(src, dst, amt, time) is not None:
        store_transaction(src, dst, float(amt), float(time), 2)
        return [-1, 'Transaction Replay']
    else:
        store_transaction(src, dst, float(amt), float(time), 0)
        return [0, 'Transaction received correctly']

def login(user, pwd):
    acc = fetch_account_by_mail(user)
    if not acc:
        return [False, 'ERROR: Incorrect Credentials', None]
    if bcrypt.checkpw(pwd.encode(), acc[3]):
        return [True, 'OK: Login Successfull', acc]
    return [False, 'ERROR: Incorrect Credentials', None]

def print_accounts():
    #for acc in fetch_accounts():
    #    print(acc[0]+' (' + acc[2] + '): ' + acc[1])
    tabledata = [[ 'Account Nº', 'KEY', 'E-mail', 'Password']] + fetch_accounts()
    table = Texttable()
    table.add_rows(tabledata)
    print(table.draw())
    return

def print_transactions():
    #for tr in fetch_transactions_toprint():
    #    print('[' + statuses()[tr[5]] + '] ' + tr[0] + ' => ' + tr[1] + ': ' + str(tr[2]) + '€ (' + str(tr[3]) + ' ' + str(tr[4]) + ')')
    tabledata = [[ 'Origin', 'Destination', 'Amount', 'Day', 'Time', 'Status']] + fetch_transactions_toprint()
    table = Texttable()
    table.add_rows(tabledata)
    print(table.draw())
    return

def resend_key(num):
    acc = fetch_account(num);
    sendMail(acc[2],'Key Recovery','Your account with number ' + acc[0] + ' has key ' + acc[1])
    print('Password re-sent correctly')
    return

def check_db(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name in ('transactions','keys')")
    return len(c.fetchall()) >= 2

def initialize_db():
    [conn, c] = get_connection()
    if check_db(c):
        conn.close()
        print('Database already initialized')
        return
    c.execute('''CREATE TABLE keys (account, key, owner, pwd)''')
    c.execute('''CREATE TABLE transactions (origin, destination, amount, time, status)''')
    conn.commit()
    conn.close()
    print('Database initialized')
    return

def get_connection():
    conn = sqlite3.connect('bank.db')
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

def fetch_account_by_mail(mail):
    [conn, c] = get_connection()
    params = (mail,)
    c.execute('SELECT * FROM keys where owner like ?',params)
    account = c.fetchone()
    conn.close()
    return account

def store_account(src, key, owner, pwd):
    acc = fetch_account(src)
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(10))
    [conn, c] = get_connection()
    if(acc is None):
        params = (src, key, owner, hashed)
        c.execute("INSERT INTO keys(account, key, owner, pwd) VALUES (?,?,?,?)", params)
    else:
        params = (key, hashed, src)
        c.execute('UPDATE keys SET key = ?, pwd = ? WHERE account = ?', params)
    conn.commit()
    conn.close()
    return

def fetch_transactions():
    [conn, c] = get_connection()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return transactions



def fetch_transactions_toprint():
    [conn, c] = get_connection()
    c.execute('SELECT origin, destination, amount, date(time), time(time), status FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return transactions

def fetch_transaction(src, dst, amt, time):
    [conn, c] = get_connection()
    params = (src, dst, amt, time)
    c.execute('SELECT * FROM transactions where origin = ? and destination = ? and amount = ? and time = ?',params)
    transaction = c.fetchone()
    conn.close()
    return transaction

def store_transaction(src, dst, amt, time, status):
    [conn, c] = get_connection()
    params = (src, dst, amt, time, status)
    c.execute('INSERT INTO transactions(origin, destination, amount, time, status) VALUES (?,?,?,?,?)',params)
    conn.commit()
    conn.close()
    return

def statuses():
    return ['OK','INCORRECT HMAC','DUPLICATE']

def statistics():
    [conn, c] = get_connection()
    c.execute('SELECT date(time), count(status) as total, \
      count(case status when 0 then 1 else null end) as ok, \
      count(case status when 1 then 1 else null end) as hmac, \
      count(case status when 2 then 1 else null end) as duplicate  \
      FROM transactions GROUP BY date(time)')
    transactions = c.fetchall()
    tabledata = [['Date','Total'] + statuses()] + transactions
    table = Texttable()
    table.add_rows(tabledata)
    print(table.draw())
    plot(transactions)
    conn.close()
    return transactions

def plot(data):
    kpi = {}
    for day in data:
        kpi[day[0]] = int(day[1])/int(day[2])
    plt.plot(list(kpi.keys()), list(kpi.values()), label='KPI')
    plt.xlabel('Day')
    plt.xlabel('KPI')
    plt.title('KPI Evolution')
    plt.savefig('KPI Evolution', dpi = 200)
