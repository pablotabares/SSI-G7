import sqlite3
from sqlite3 import Error
import json

def create_db():
    try:
        con = sqlite3.connect('database.db')
        print('Connection established => Database created')
        return con
    except Error:
        print(Error)

def sql_table(con):

    keys = {"123456": "alsdkgousf56ds4g98we", "89876": "asdgpsddf8dsg5", "4852": "14587412fsev"}
    data = json.dumps(keys)

    cursor = con.cursor()
    #cursor.execute("CREATE TABLE clients(accountNumber integer PRIMARY KEY, hmac integer)")
    #con.commit()
    
    for i in data:
        entities = (i, [i])
        print(entities)
        #cursor.execute('''INSERT INTO clients(accountNumber, hmac) VALUES(?, ?)''', entities)

        #con.commit()


con = create_db()    
sql_table(con)
