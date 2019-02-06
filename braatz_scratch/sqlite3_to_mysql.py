import sqlite3
import os
import time
import mysql.connector
import json

cursor = None
mydb = None

def mysql_connection():
    global cursor, mydb
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
        cursor = mydb.cursor()
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
    # Create Table
    create_string = "CREATE TABLE " + table + ' ('
    idx = 0
    for col in data[table]['table_col']:

        #  Datatype Replacements
        if str.upper(data[table]['table_col'][col]['datatype']) == "":
            datatype = 'VARCHAR(20)'
        elif str.upper(data[table]['table_col'][col]['datatype']) == "VARCHAR(100)":
            datatype = "VARCHAR(400)"
        elif str.upper(data[table]['table_col'][col]['datatype']) == "REAL":
            datatype = "FLOAT"
        else:
            datatype = str.upper(data[table]['table_col'][col]['datatype'])

        #  Name Replacements
        if data[table]['table_col'][col]['name'] == "key":
            name = "key_"
        else:
            name = data[table]['table_col'][col]['name']

        #  Character Set
        if 'utf8' in data[table]['table_col'][col]:
            character_set = ' CHARACTER SET utf8 COLLATE utf8_unicode_ci'
        else:
            character_set = ''

        if idx != 0:
            create_string += ', '
        create_string += name + ' ' + datatype + character_set
        idx += 1
    create_string += ');'
    print(create_string)
    cursor.execute(create_string)
    mydb.commit()

    # Add Data
    for row in data[table]['table_dat']:
        add_string = r'INSERT INTO ' + table + r' VALUES ('
        idx = 0
        for col in row:
            flag = False
            if isinstance(col, str):
                if '"' in col:
                    col = col.replace('"', r'\"')
                if "'" in col:
                    col = col.replace("'", r"\'")

            if idx != 0:
                add_string += r', '
            add_string += '"' + str(col) + '"'
            idx += 1
        add_string += r');'
        try:
            cursor.execute(add_string)
            mydb.commit()
        except:
            print(add_string + " Failed.")


def unicode(table, col_2_unicode):
    for idx, row in enumerate(data[table]['table_dat']):
        for col in col_2_unicode:
            data[table]['table_dat'][idx][col] = data[table]['table_dat'][idx][col].encode('utf-8')

mysql_connection()

data = sqlite3_dumb()
table_time_conv(data['spytify_play'])

needs_unicode = {
    'spytify_play': ['device'],
    'spytify_song': ['name'],
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

    transfer(table)

cursor.close()
mydb.close()



