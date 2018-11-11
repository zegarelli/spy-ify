import sqlite3
import pandas as pd
import datetime


def album():
    c.execute("INSERT INTO albums VALUES (?,?,?,?,?,?,?)",
                      (id,
                       f['name'],
                       f['artists'][0]['id'],
                       f['label'],
                       f['popularity'],
                       f['album_type'],
                       f['release_date'],
                       ))

db = sqlite3.connect('spotify_data.db')
cursor = db.cursor()

dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()

# Add Users to DB
users = cursor.execute("SELECT * FROM users").fetchall()
for n, user in enumerate(users):
    try:
        c.execute("INSERT INTO spytify_user VALUES (?,?,?,?,?,?,?)",
              (n+1, user[2], user[0], user[1], '1993-06-09', '1993-06-09', 'M'))
        dj.commit()
    except Exception as e:
        print(e)

# Add Artists to DB
artists = cursor.execute("SELECT * FROM artists").fetchall()
for n, artist in enumerate(artists):
    try:
        c.execute("INSERT INTO spytify_artist VALUES (?,?,?,?,?)",
              (artist[0], artist[1], artist[3], artist[4], artist[2]))
        dj.commit()
    except Exception as e:
        print(e)

# Add Albums to DB
albums = cursor.execute("SELECT * FROM albums").fetchall()
for n, album, in enumerate(albums):
    try:
        c.execute("INSERT INTO spytify_album VALUES (?,?,?,?,?,?,?)",
              (album[0], album[1], album[3], album[4], album[5], album[2], album[6]))
        dj.commit()
    except Exception as e:
        print(e)


# Add Songs to DB
songs = cursor.execute("SELECT * FROM songs").fetchall()
for n, song, in enumerate(songs):
    try:
        c.execute("INSERT INTO spytify_song VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (song[0], song[3], song[4], song[5], song[6], song[7], song[8], song[9], song[10], song[11], song[12],
               song[13], song[15], song[16], song[17], song[18], song[2], song[1], song[14]))
        dj.commit()
    except Exception as e:
        print(e)


# Add Plays to DB
plays = cursor.execute("SELECT * FROM plays").fetchall()
for n, play, in enumerate(plays):
    if n > 3019:
        try:
            c.execute("INSERT INTO spytify_play VALUES (?,?,?,?,?)",
                  (n, play[0], play[3], play[1], play[2]))
            dj.commit()
        except Exception as e:
            print(e)

dj.close()
db.close()