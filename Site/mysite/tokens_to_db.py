import sqlite3
import os
import json

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
users = cursor.execute("""Select * from auth_user""").fetchall()
for user in users:
    cache_path = r'spotify_api/token_cache/'
    for file in os.listdir(cache_path):
        if user[6] == file[7:]:
            file = open('{}{}'.format(cache_path, file))
            file = file.read()
            data = json.loads(file)
            cursor.execute("""INSERT INTO spytify_usertoken (id, access_token, token_type, expires_in, scope, expires_at,
                            refresh_token, user_id) VALUES (?,?,?,?,?,?,?,?)""",
                           (user[0], data['access_token'], data['token_type'], data['expires_in'], data['scope'],
                            data['expires_at'], data['refresh_token'], user[0]))
            db.commit()
