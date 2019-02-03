import sqlite3
import os
import time
import mysql.connector
import json

def mysql_connection():
    who = "jax_auto"
    with open('auth.json') as f:
        cred = json.load(f)
    mydb = mysql.connector.connect(
        host=cred[who]['host'],
        user=cred[who]['user'],
        passwd=cred[who]['pass'],
        database="spyify"
    )

    mycursor = mydb.cursor()

    print('hi')

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
                'datetype': col[2]
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


mysql_connection()

data = sqlite3_dumb()
table_time_conv(data['spytify_play'])



