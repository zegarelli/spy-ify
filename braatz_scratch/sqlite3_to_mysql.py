import sqlite3
import os
import time
import json
import psycopg2

cursor = None
mydb = None

def mysql_connection():
    global cursor, mydb
    try:
        mydb = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(
            os.environ['DB_NAME'],
            os.environ['DB_USER'],
            os.environ['DB_HOST'],
            os.environ['DB_PASSWORD'],

        ))
        cursor = mydb.cursor()
    except:
        print("I am unable to connect to the database")

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

    date_time = time_d['year'] + '-' + time_d['month'] + '-' + time_d['day'] + ' ' +  time_d['hour'] + ':' + time_d['minute'] + ':0'
    return date_time

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
        for idx, col in enumerate(cols):
            dicks[table_name]['table_col'][col[1]] = {
                'name': col[1],
                'datatype': col[2],
                'id': idx
            }
        table = cursor.execute("SELECT * from %s" % table_name).fetchall()
        for row_dat in table:
            row_dat = list(row_dat)
            dicks[table_name]['table_dat'].append(row_dat)
    return dicks

def table_time_conv(table):
    for id, row in enumerate(table['table_dat']):
        table['table_dat'][id][1] = dumb_string_2_epoch(table['table_dat'][id][1])


def transfer(table):
    columns = data[table]['table_col']
    column_names = []
    for column in columns:
        column_names.append(column)
    column_str = '(' + ','.join(column_names) + ')'
    for row in data[table]['table_dat']:
        add_string = r'INSERT INTO ' + table + ' ' + column_str + r' VALUES ('
        idx = 0
        for col in row:
            empty = False
            if isinstance(col, bytes):
                col = col.decode('utf-8')
            if isinstance(col, str):
                if "'" in col:
                    col = col.replace("'", r"''")
            if col == "" or col == None or col == 'None':
                col = "NULL"
                empty = True
            if idx != 0:
                add_string += r', '
            if empty:
                add_string += str(col)
            else:
                add_string += "'" + str(col) + "'"
            idx += 1
        add_string += r');'
        try:
            cursor.execute(add_string)
            mydb.commit()
        except Exception as e:
            cursor.execute('END TRANSACTION;')
            print(e)
            print("FAILED: " + add_string)


def unicode(table, col_2_unicode):
    for idx, row in enumerate(data[table]['table_dat']):
        for col in col_2_unicode:
            if data[table]['table_dat'][idx][col] == None:
                data[table]['table_dat'][idx][col] = ''
            data[table]['table_dat'][idx][col] = data[table]['table_dat'][idx][col].encode('utf-8')

mysql_connection()

data = sqlite3_dumb()
table_time_conv(data['spytify_play'])

needs_unicode = {
    'spytify_play': ['device'],
    'spytify_song': ['song_name'],
    'spytify_artist': ['artist_name', 'genre'],
    'spytify_album': ['album_name', 'label'],
    'auth_user': ['username', 'firstname', 'lastname']
}

for table in data:

    if table in needs_unicode:
        col_2_unicode = []
        for col in data[table]['table_col']:
            if col in needs_unicode[table]:
                data[table]['table_col'][col]['utf8'] = True
                col_2_unicode.append(data[table]['table_col'][col]['id'])
        unicode(table, col_2_unicode)

    if table == 'spytify_album':
        transfer(table)

cursor.close()
mydb.close()



