import sqlite3
import pandas as pd
import datetime

db = sqlite3.connect('spotify_data.db')
cursor = db.cursor()

dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()

# Add Artists to DB
# artists = cursor.execute("SELECT * FROM artists").fetchall()
# c.execute("DELETE FROM spytify_artist")
# dj.commit()
# for n, artist in enumerate(artists):
#     try:
#         c.execute("""INSERT INTO spytify_artist (artist_id,artist_name,genres,followers,artist_popularity) VALUES
#                   (?,?,?,?,?)""", (artist[0], artist[1], artist[2], artist[3], artist[4]))
#         dj.commit()
#     except Exception as e:
#         print(e)

# Add Albums to DB
# albums = cursor.execute("SELECT * FROM albums").fetchall()
# c.execute("DELETE FROM spytify_album")
# dj.commit()
# for n, album, in enumerate(albums):
#     try:
#         c.execute("""INSERT INTO spytify_album (album_id,album_name,artist_id_id,label,album_popularity,album_type,
#         release_date) VALUES (?,?,?,?,?,?,?)""", (album[0], album[1], album[2], album[3], album[4], album[5], album[6]))
#         dj.commit()
#     except Exception as e:
#         print(e)


# Add Songs to DB
# songs = cursor.execute("SELECT * FROM songs").fetchall()
# c.execute("DELETE FROM spytify_song")
# dj.commit()
# for n, song, in enumerate(songs):
#     try:
#         c.execute("""INSERT INTO spytify_song (song_id, artist_id_id, album_id_id, song_name, song_popularity,
#                   danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
#                   valence, tempo,type, duration_ms, time_signature) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
#                   (song[0], song[1], song[2], song[3], song[4], song[5], song[6], song[7], song[8], song[9], song[10],
#                    song[11], song[12], song[13], song[14], song[15], song[16], song[17], song[18]))
#         dj.commit()
#     except Exception as e:
#         print(e)


# Add Plays to DB
plays = cursor.execute("SELECT * FROM plays").fetchall()
c.execute("DELETE FROM spytify_play")
dj.commit()
for n, play, in enumerate(plays):
    if n > 3019:
        try:
            c.execute("""INSERT INTO spytify_play (play_id, time_stamp, user_id, song_id, device) VALUES (?,?,?,?,?)""",
                      (n, play[0], play[1], play[2], play[3]))
            dj.commit()
        except Exception as e:
            print(e)

dj.close()
db.close()