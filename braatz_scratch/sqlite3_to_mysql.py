import sqlite3
import os
import time
import mysql.connector
import json

mydb = None

def mysql_connection():
    global mydb
    """
    Note: This requires .json with credentials to access jmoney.cash MySQL server.
    Replace who with given credentials.
    Request credentials from jmoney.cash admin.
    """
    who = "jax_auto"
    with open('auth.json') as f:
        cred = json.load(f)
    try:
        mydb = mysql.connector.connect(
            host=cred[who]['host'],
            user=cred[who]['user'],
            passwd=cred[who]['pass'],
            database="spyify"
        )

        if mydb.is_connected():
            print('Connected to MySQL database. Thank you for choosing Jmoney.Cash')
    except EnvironmentError as e:
        print(e)

def dumb_string_2_epoch(dumb_string):
    string = dumb_string.split(' ')
    string_day = string[1]
    string_day = string_day.split('/')
    string_time = string[2]
    string_time = string_time.split(':')
    time_d = {
        'day': string_day[1],
        'month': string_day[0],
        'year': string_day[2],
        'hour': string_time[0],
        'minute': string_time[1]
    }

    date_time = time_d['day'] + '.' + time_d['month'] + '.' + time_d['year'] + ' ' +  time_d['hour'] + ':' + time_d['minute'] + ':0'
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return  epoch

def sqlite3_dumb():
    dicks = {}
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        dicks[table_name] = {
            'table_col': {},
            'table_dat': []
        }
        cols = cursor.execute("PRAGMA table_info(%s);" % table_name).fetchall()
        for col in cols:
            dicks[table_name]['table_col'][col[1]] = {
                'name': col[1],
                'datatype': col[2]
            }
        # sleep(1)
        table = cursor.execute("SELECT * from %s" % table_name).fetchall()
        for row_dat in table:
            row_dat = list(row_dat)
            dicks[table_name]['table_dat'].append(row_dat)
    return dicks

def table_time_conv(table):
    for id, row in enumerate(table['table_dat']):
        table['table_dat'][id][1] = dumb_string_2_epoch(table['table_dat'][id][1])

def mysql_table_maker(table):
    table['d']


def transfer(table):
    # Create Table
    create_string = "CREATE TABLE " + table + ' ('
    idx = 0
    for col in data[table]['table_col']:
        if idx != 0:
            create_string += ', '
        create_string += data[table]['table_col'][col]['name'] + ' ' + str.upper(data[table]['table_col'][col]['datatype'])
        idx += 1
    create_string += ');'
    # Add Data
    for row in data[table]['table_dat']:
        print(row)

mysql_connection()

# mydb.cursor('SELECT * from test;')

data = sqlite3_dumb()
table_time_conv(data['spytify_play'])

for table in data:
    transfer(table)



